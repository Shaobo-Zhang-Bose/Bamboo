#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Organization  BOSE CORPORATION
#  Copyright     COPYRIGHT 2020 BOSE CORPORATION ALL RIGHTS RESERVED.
#                This program may not be reproduced, in whole or in part in any
#                form or any means whatsoever without the written permission of
#                    BOSE CORPORATION
#                    The Mountain,
#                    Framingham, MA 01701-9168
#  Team          China 2.0 Eng
###############################################################################
"""
Description  : Support voice query for Xiaowei
"""
from wham_automation.JiraKnownIssues import KnownIssue

__docformat__ = 'restructuredtext en'
__author__ = 'Shaobo Zhang'

import os
import pyaudio
import wave
import sys
import pyttsx3
import re
import requests
import time
import base64
from pyaudio import PyAudio, paInt16
from threading import Thread, Event, Condition
from datetime import datetime

from wham_automation.lib.framework.Configs.FrameworkConstants import PhoneType
from wham_automation.lib.mobile.scenario.PhoneObject import PhoneAppType
from wham_automation.script_support.AssertHelpers import SinkStates
from wham_automation.lib.framework.Configs.ProductInfo import Buttons
from wham_automation.script_support.ScriptHelper import wait
from wham_automation.utils.log import logger
from wham_automation.lib.mobile.constants.MobileConstants import const

class XiaoweiSupport:
    @classmethod
    def xw_query_response_dict(cls):
        day = datetime.now().isoweekday()
        day_of_week_dict = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "天"}
        weekday_dict = {
            "今天星期几": "今天是星期" + day_of_week_dict[day],
            "明天星期几": "明天是星期" + (day_of_week_dict[1] if day == 7 else day_of_week_dict[day + 1]),
            "昨天星期几": "昨天是星期" + (day_of_week_dict[7] if day == 1 else day_of_week_dict[day - 1])
        }
        weather_dict = {
            "上海的天气": "上海.*温度.*空气.*",
            "北京的天气": "北京.*温度.*空气.*",
            "广州的天气": "广州.*温度.*空气.*",
            "深圳的天气": "深圳.*温度.*空气.*"
        }
        festival_dict = {
            "春节的习俗": "春节.*农历.*",
            "元宵节的习俗": "元宵节.*农历正月十五.*",
            "重阳节的习俗": "重阳节.*农历九月初九.*",
            "清明节的习俗": "清明节.*传统.*"
        }
        long_query_dict = {
            "江碧鸟逾白山青花欲燃今春看又过何日是归年": ".*绝句二首.*"
        }                   
        query_response_dict = dict()
        query_response_dict["query_weekday"] = weekday_dict
        query_response_dict["query_weather"] = weather_dict
        query_response_dict["query_festival"] = festival_dict
        query_response_dict["long_query"] = long_query_dict                                                          
        return query_response_dict

    @classmethod
    def xw_control_story_or_music(cls):
        story_music_dict = {
            "播放故事": "好的.*播放.*",
        }
        control_playing_dict = {
            "decrease_volume": "声音小一点",
            "increase_volume": "声音大一点",
            "pause_playing": "暂停播放",
            "resume_playing": "继续播放",
            "play_next": "播放下一首",
            "play_previous": "播放上一首"
        }

        control_story_or_music = dict()
        control_story_or_music["story_music_dict"] = story_music_dict
        control_story_or_music["control_dict"] = control_playing_dict
        return control_story_or_music

    @classmethod
    def xw_in_translation_mode(cls):
        translation_mode_dict = {
            "goto_translation_mode": {"进入翻译模式": "已进入翻译，请说出需要翻译的内容，如需退出，请说退出翻译"},
            "quit_translation_mode": {"退出翻译": "已退出翻译"},
            "translation_sentence": {"请为我翻译这句话": "Please translate this sentence for me."}
        }
        return translation_mode_dict                
    verify_vpa_status = None

    @classmethod
    def test_vpa(cls, dut, query_words, button=Buttons.VPA, hold_seconds=5, how_many_times=1, phone=None,
                 turn_off_network=False, turn_off_bluetooth=False, close_xiaowei=False):
        wait(3)
        press_vpa_button = VPAProcess(dut, button, hold_seconds, how_many_times)
        if phone and turn_off_network:
            if not phone.launch_application(PhoneAppType.SETTINGS):
                return False
            if not phone.settings.cellular_off():
                return False
            phone_setting = PhoneSetting(phone, setting="network")
            phone_setting.start()
            wait(5, "network will be turned off")
            press_vpa_button.start()
            play_vpa_voice = GenerateVoiceToQuery(query_words)
            play_vpa_voice.play_query_voice()
            phone_setting.join()
            if not phone_setting.get_result():
                return False

        elif phone and turn_off_bluetooth:
            if not phone.launch_application(PhoneAppType.SETTINGS):
                return False
            phone_setting = PhoneSetting(phone, setting="bluetooth")
            phone_setting.start()
            wait(8, "bluetooth will be turned off")
            press_vpa_button.start()
            play_vpa_voice = GenerateVoiceToQuery(query_words)
            play_vpa_voice.play_query_voice()
            phone_setting.join()
            if not phone_setting.get_result():
                return False

        elif phone and close_xiaowei:
            press_vpa_button.start()
            play_vpa_voice = GenerateVoiceToQuery(query_words)
            play_vpa_voice.play_query_voice()
            wait(2)
            if not phone.xiaowei.terminate_app():
                return False

        else:
            press_vpa_button.start()
            play_vpa_voice = GenerateVoiceToQuery(query_words)
            play_vpa_voice.play_query_voice()

        press_vpa_button.join()
        cls.verify_vpa_status = VerifyVPAStatus(dut, phone)
        return True

    @classmethod
    def test_swipe_forward_back(cls, forward=False, back=False):
        test_result = cls.verify_vpa_status.verify_dut_sink_state_while_swipe_captouch_forward_back(forward, back)
        return test_result

    @classmethod
    def test_swipe_up_down(cls):
        test_result = cls.verify_vpa_status.verify_volume_level_while_swipe_captouch_up_down()
        return test_result

    @classmethod
    def test_double_tap(cls, pause_streaming=False, resume_streaming=False):
        test_result = cls.verify_vpa_status.verify_streaming_pause_resume_while_double_tap_captouch(pause_streaming, resume_streaming)
        return test_result

    @classmethod
    def test_interruption(cls):
        test_result = cls.verify_vpa_status.verify_dut_sink_state_while_previous_response_was_interrupted()
        return test_result

    @classmethod
    def test_discoverable_state(cls):
        test_result = cls.verify_vpa_status.verify_dut_sink_state_while_dut_in_discoverable_state()
        return test_result

    @classmethod
    def test_story_music(cls):
        test_result = cls.verify_vpa_status.verify_dut_sink_state_while_dut_is_playing_music()
        return test_result

    @classmethod
    def test_a2dp_source(cls):
        test_result = cls.verify_vpa_status.verify_dut_sink_state_and_check_a2dp_source()
        return test_result

    @classmethod                                        
    def test_xiaowei_vpa(cls):
        test_result = cls.verify_vpa_status.verify_dut_sink_state()
        return test_result

    @classmethod
    def test_native_vpa(cls):
        test_result = cls.verify_vpa_status.verify_dut_sink_state(test_native_vpa=True)
        return test_result

    @classmethod
    def get_current_dut_sink_state(cls):
        test_result = cls.verify_vpa_status.get_dut_sink_state()
        return test_result

    @classmethod      
    def test_query_no_response(cls):
        return True

    @classmethod
    def download_xiaowei(cls, phone):
        if phone.phone_type == PhoneType.ANDROID:
            phone.launch_application(PhoneAppType.BLUETOOTH)
            driver = phone._current_app.driver.appium_driver
            logger.info("downloading xiaowei")
            appUrl = r'https://imtt.dd.qq.com/16891/apk/EE10B0EEF0826192921AF851952191E5.apk?fsname=com.tencent.xw'
            driver.install_app(appUrl)

        if phone.phone_type == PhoneType.IOS:
            bundle_id = 'com.apple.AppStore'
            app_current_status = driver.execute_script('mobile: queryAppState', {'bundleId': bundle_id})
            if app_current_status == const.APPLICATION_NOT_RUNNING or app_current_status == \
                    const.APPLICATION_RUNNING_IN_BACKGROUND:
                driver.execute_script('mobile: activateApp', {'bundleId': bundle_id})
            else:
                driver.execute_script('mobile: launchApp', {'bundleId': bundle_id})
            search_bar_xpath = '//XCUIElementTypeSearchField'
            xiaowei_download_xpath = '//XCUIElementTypeButton[contains(@name,"腾讯小微")]//XCUIElementTypeButton'
            xiaowei_open_xpath = '//XCUIElementTypeButton[contains(@name,"腾讯小微")]//XCUIElementTypeButton[@name="open"]'
            search_tab_xpath = '//*[@name="Search"]'

            search_tab = cls.wait_find_element(driver, search_tab_xpath)
            if search_tab is not None:
                logger.debug("search tab is found")
                search_tab.click()
            else:
                logger.debug("search tab is not found")
                return False

            search_bar = cls.wait_find_element(driver, search_bar_xpath)
            if search_bar is not None:
                logger.debug("search bar is found")
                search_bar.clear()
                search_bar.send_keys("腾讯小微"+"\n")
            else:
                logger.debug("search bar is not found")
                return False

            open_btn = cls.wait_find_element(driver, xiaowei_open_xpath)
            if open_btn is not None:
                logger.debug("open button is found")
                return True
            else:
                logger.debug("open button is not found")

            download_btn = cls.wait_find_element(driver, xiaowei_download_xpath)
            if download_btn is not None:
                logger.debug("download button is found")
                download_btn.click()
            else:
                logger.debug("download button is not found")
                return False
            return True

    @classmethod
    def wait_find_element(self, driver, element_xpath, wait_time=2):
            element = None
            try:
                isfound = self.wait_till_element_to_be_visible(driver, element_xpath, wait_time)
                if isfound:
                    element = driver.find_element_by_xpath(element_xpath)
            except Exception as e:
                pass
            finally:
                return element

class GenerateVoiceToQuery:
    def __init__(self, query_words, voice_rate=120):
        self.query_words = query_words
        self.rate = voice_rate
        self.engine = pyttsx3.init()

    def start_voice_query(self, name):
        logger.info("Start conducting a %s : %s" % (name, self.query_words))

    def finish_voice_query(self, name, completed):
        if completed:
            logger.info("The %s is over" % name)
            self.engine.endLoop()
        else:
            logger.error("There is an exception when %s" % name)
            self.engine.endLoop()

    def play_query_voice(self):
        self.engine.setProperty('rate', self.rate)

        if sys.platform == 'win32':
            self.engine.setProperty("voice",
                                    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
        if sys.platform == 'darwin':
            self.engine.setProperty("voice",
                                    r"com.apple.speech.synthesis.voice.ting-ting")
        wait(1)
        self.engine.connect('started-utterance', self.start_voice_query)
        self.engine.connect('finished-utterance', self.finish_voice_query)
        self.engine.say(self.query_words, "xiaowei vpa query")

        self.engine.startLoop()
        # self.engine.runAndWait()
        self.engine.disconnect({"topic": 'started-utterance', "cb": self.start_voice_query})
        self.engine.disconnect({"topic": 'finished-utterance', "cb": self.finish_voice_query})

class PhoneSetting(Thread):
    def __init__(self, phone, setting):
        Thread.__init__(self)
        self.phone = phone
        self.setting = setting

    def run(self):
        self.perform_setting_result = self.perform_setting()

    def perform_setting(self):
        if self.setting == "network":
            if not self.phone.launch_application(PhoneAppType.SETTINGS):
                return False
            if not self.phone.settings.wifi_off():
                return False
            if not self.phone.settings.terminate_app():
                return False
        elif self.setting == "bluetooth":
            if not self.phone.launch_application(PhoneAppType.BLUETOOTH):
                return False
            if not self.phone.bluetooth.bt_radio(enable='off'):
                return False
            if not self.phone.settings.terminate_app():
                return False
        else:
            pass

        return True

    def get_result(self):
        return self.perform_setting_result

class SwipeCapTouchForwardBack(Thread):
    def __init__(self, dut, forward, back):
        Thread.__init__(self)
        self.dut = dut
        self.forward = forward
        self.back = back

    def run(self):
        if self.forward and self.back:
            self.perform_forward_gesture_result = self.perform_forward_gesture()
            self.perform_back_gesture_result = self.perform_back_gesture()
            self.perform_forward_back_gestures_result = self.perform_forward_gesture_result and self.perform_back_gesture_result
        elif self.forward and not self.back:
            self.perform_forward_gesture_result = self.perform_forward_gesture()
            self.perform_forward_back_gestures_result = self.perform_forward_gesture_result
        elif not self.forward and self.back:
            self.perform_back_gesture_result = self.perform_back_gesture()
            self.perform_forward_back_gestures_result = self.perform_back_gesture_result
        else:
            return False

    def perform_forward_gesture(self):
        self.dut.captouch.captouch_swipe_forward()
        wait(3)
        if self.dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
            return True
        else:
            return False

    def perform_back_gesture(self):
        self.dut.captouch.captouch_swipe_back()
        wait(3)
        if self.dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
            return True
        else:
            return False

    def get_result(self):
        return self.perform_forward_back_gestures_result

class SwipeCapTouchUpDown(Thread):
    def __init__(self, dut):
        Thread.__init__(self)
        self.dut = dut
        self.max_volume = 16
        self.min_volume = 0

    def run(self):
        self.perform_down_gesture_result = self.perform_down_gesture()
        self.perform_up_gesture_result = self.perform_up_gesture()
        self.perform_up_down_gestures_result = self.perform_up_gesture_result and self.perform_down_gesture_result

    def perform_up_gesture(self):
        for i in range(20):
            self.dut.captouch.captouch_swipe_up()
            if self.dut.status.get_volume() == self.max_volume:
                return True
            else:
                wait(0.5)
        return False

    def perform_down_gesture(self):
        for i in range(20):
            self.dut.captouch.captouch_swipe_down()
            if self.dut.status.get_volume() == self.min_volume:
                return True
            else:
                wait(0.5)
        return False

    def get_result(self):
        return self.perform_up_down_gestures_result

class DoubleTapCapTouch(Thread):
    def __init__(self, dut, pause_streaming, resume_streaming):
        Thread.__init__(self)
        self.dut = dut
        self.pause_streaming = pause_streaming
        self.resume_streaming = resume_streaming

    def run(self):
        wait(2)
        self.perform_double_tap_result = self.perform_double_tap_gesture()

    def perform_double_tap_gesture(self):
        if self.pause_streaming and not self.resume_streaming:
            self.dut.captouch.captouch_double_tap()
            for i in range(5):
                wait(5)
                if self.dut.status.get_sink_state() == SinkStates.CONNECTED:
                    return True
                else:
                    wait(5)
            return False
        elif not self.pause_streaming and self.resume_streaming:
            self.dut.captouch.captouch_double_tap()
            for i in range(5):
                wait(5)
                if self.dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
                    return True
                else:
                    wait(5)
            return False
        else:
            if not self.dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
                return False
            self.dut.captouch.captouch_double_tap()
            wait(5)
            if self.dut.status.get_sink_state() == SinkStates.CONNECTED:
                return True
            else:
                return False

    def get_result(self):
        return self.perform_double_tap_result

class CheckA2DPSource(Thread):
    def __init__(self, dut, phone):
        Thread.__init__(self)
        self.dut = dut
        self.phone = phone

    def run(self):
        self.check_result = self.check_qq_music_pause_state()

    def check_qq_music_pause_state(self):
        wait(1)
        active_app = self.phone.qqmusic.activate_app()
        click_no_reminder_button = self.phone.qqmusic.no_reminder_for_music_interruption()
        pause_music = self.phone.qqmusic.pause_music()
        if active_app and click_no_reminder_button and pause_music:
            if self.dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
                logger.info("QQ music has been paused, streaming is come from VPA response")
                return True

    def get_result(self):
        return self.check_result

class VPAProcess(Thread):
    def __init__(self, dut, button, hold_seconds, how_many_times):
        Thread.__init__(self)
        self.dut = dut
        self.button = button
        self.hold_seconds = hold_seconds
        self.how_many_times = how_many_times

    def run(self):
        self.perform_vpa_gestures()

    def perform_vpa_gestures(self):
        self.dut.manager.vpa_tap_hold(hold_seconds=self.hold_seconds, how_many_times=self.how_many_times)

class VerifyVPAStatus:
    def __init__(self, dut, phone):
        self.dut = dut
        self.phone = phone                  

    def verify_dut_sink_state_while_previous_response_was_interrupted(self):
        for i in range(10):
            if self.dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
                return True
            else:
                wait(1)
        return False

    def verify_dut_sink_state_while_swipe_captouch_forward_back(self, forward, back):
        wait(3)
        perform_forward_back_gestures = SwipeCapTouchForwardBack(self.dut, forward, back)
        perform_forward_back_gestures.start()
        perform_forward_back_gestures.join()
        return perform_forward_back_gestures.get_result()

    def verify_volume_level_while_swipe_captouch_up_down(self, forward=False, back=False):
        wait(3)
        perform_up_down_gestures = SwipeCapTouchUpDown(self.dut)
        perform_up_down_gestures.start()
        perform_up_down_gestures.join()
        return perform_up_down_gestures.get_result()

    def verify_streaming_pause_resume_while_double_tap_captouch(self, pause_stream, resume_streaming):
        perform_double_tap_gesture = DoubleTapCapTouch(self.dut, pause_stream, resume_streaming)
        perform_double_tap_gesture.start()
        perform_double_tap_gesture.join()
        return perform_double_tap_gesture.get_result()

    def verify_qqmusic_pause_while_vpa_response_streaming(self, pause_stream, resume_streaming):
        perform_double_tap_gesture = DoubleTapCapTouch(self.dut, pause_stream, resume_streaming)
        perform_double_tap_gesture.start()
        perform_double_tap_gesture.join()
        return perform_double_tap_gesture.get_result()

    def verify_dut_sink_state_while_dut_in_discoverable_state(self):
        for i in range(10):
            if self.dut.status.get_sink_state() == SinkStates.DISCOVERABLE:
                return True
            else:
                wait(1)
        return False

    def verify_dut_sink_state_while_dut_is_playing_music(self):
        wait(10)
        if self.dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
            return True

        else:
            return False

    def verify_dut_sink_state_and_check_a2dp_source(self):
        wait(5)
        check_a2dp_source = CheckA2DPSource(self.dut, self.phone)
        check_a2dp_source.start()
        check_a2dp_source.join()
        test_result = check_a2dp_source.get_result()
        if test_result:
            resume_music = self.phone.qqmusic.music_resuming_after_interruption()
            if resume_music:
                if self.get_dut_sink_state() == SinkStates.A2DP_STREAMING:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return test_result

    def get_dut_sink_state(self):
        wait(5)
        return self.dut.status.get_sink_state()

    def verify_dut_sink_state(self, test_native_vpa=False):
        count = 0
        ss_a2dp_streaming = False
        ss_active_call_sco = False
        ss_no_call_sco = False                      
        ss_connected = False

        while count < 10:
            # If sink state of dut has not changed to A2DP_STREAMING or ACTIVE_CALL_SCO within 10s after releasing VPA button, the test fail
            logger.info("Check if the ss has changed to A2DP_STREAMING")
            if self.dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
                logger.info("waiting for response to play")
                ss_a2dp_streaming = True
                break
            elif self.dut.status.get_sink_state() == SinkStates.ACTIVE_CALL_SCO:
                logger.info("waiting for response to play")
                ss_active_call_sco = True
                break
            elif self.dut.status.get_sink_state() == SinkStates.DEVICE_NO_CALL_SCO:
                logger.info("waiting for response to play")
                ss_no_call_sco = True
                break
            else:
                wait(1)
                count += 1
        if not (ss_a2dp_streaming or ss_active_call_sco or ss_no_call_sco):
            return False
        else:
            # If sink state of dut has not changed to CONNECTED within 250s after playing a2dp stream, the test fail
            count = 0
            while count < 250:
                logger.info("Check if the ss has changed to CONNECTED")
                if self.dut.status.get_sink_state() == SinkStates.CONNECTED:
                    logger.info("VPA response is over")
                    ss_connected = True
                    break
                else:
                    wait(1)
                    count += 1
            if ss_a2dp_streaming and ss_connected:
                return True
            elif test_native_vpa and ss_active_call_sco and ss_connected:
                return True
            else:
                return False
