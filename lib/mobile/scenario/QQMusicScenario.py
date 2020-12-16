import subprocess
from subprocess import PIPE
import time
import os
import pyaudio
import wave
import re
from threading import Thread
from datetime import datetime
from enum import unique, Enum
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.wait import WebDriverWait

from wham_automation.script_support import Precondition
from wham_automation.utils.ConfigParser import get_appium_server_ip, get_android_madrid_app_package
# get_android_willow_app_activity, get_willow_login_user_name, get_willow_login_user_password
from wham_automation.lib.mobile.scenario.BasePage import BasePage
from wham_automation.script_support.ScriptHelper import wait
from wham_automation.lib.framework.Configs.FrameworkConstants import PhoneType
from wham_automation.script_support.ScriptHelper import wait_until_step
from wham_automation.utils.log import logger
from wham_automation.test_scripts.Bamboo.lib.mobile.constants import HUAWEIConstant, XIAOMIConstant
from wham_automation.lib.framework.Configs.ProductInfo import Buttons
from wham_automation.script_support.AssertHelpers import SinkStates
from wham_automation.test_scripts.Bamboo.VPA_Xiaowei.Xiaowei_Support import VPAProcess
from appium.webdriver.common.touch_action import TouchAction

MAX_DUT_TO_SEARCH_IN_CAROUSEL = 2


class QQMusicScenario(BasePage):
    pre_check_result = False

    def __initialize_variable_of_qqmusic_app(self):
        """
        Initialize all variable used in Willow application
        """
        if self.phone_info.phone_type == PhoneType.ANDROID:
            self.package_name = 'com.tencent.qqmusic'
            self.activity_name = 'com.tencent.qqmusic.activity.AppStarterActivity'
            self.play_music_label = '//android.widget.ImageView[@content-desc="播放"]'
            self.pause_music_label = '//android.widget.ImageView[@content-desc="暂停"]'
            self.music_interruption_pop_window = '//android.widget.TextView[@text="检测到被其他应用中断播放，是否打开允许与其他应用同时播放？"]'
            self.music_interruption_no_reminder_button = '//android.widget.Button[@text="不再提醒"]'
            self.close_membership_application_button = '//android.widget.ImageView[@content-desc="关闭"]'

        if self.phone_info.phone_type == PhoneType.IOS:
            self.package_name = 'com.tencent.QQMusic'
            self.activity_name = 'com.tencent.QQMusic'
            self.music_interruption_no_reminder_button = '//XCUIElementTypeButton[@name="不再提醒"]'
            self.close_membership_application_button = '//XCUIElementTypeButton[@name=="关闭"]'

            self.play_or_pause_music_button = '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1] \
                /XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1] \
                /XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]/XCUIElementTypeButton[1]'

    def launch_qqmusic_app(self, driver=None):
        """
        Launch willow application
        :param:None
        :return:None
        :raises:None
        """
        try:
            wait(5)
            self.__initialize_variable_of_qqmusic_app()
            if driver:
                self.driver = driver
            else:
                self.driver = self.mobile_driver_factory_object.get_driver(get_appium_server_ip(),
                                                                           self.phone_info.appium_port,
                                                                           self.phone_info.platform_name,
                                                                           self.phone_info.os_version,
                                                                           self.phone_info.config_name,
                                                                           self.phone_info.uuid,
                                                                           self.package_name,
                                                                           self.activity_name,
                                                                           self.phone_info.wda_local_port)
        except Exception as e:
            logger.error(f'Driver launch  Fail on {self.phone_info.bluetooth_name}')
            logger.error(repr(e))
            return False
        else:
            return True

    def close_pop_window(self, wait_time=5):
        wait(5, 'If there is a pop window, close it')
        try:
            WebDriverWait(self.driver.appium_driver, wait_time, 1).until(
                lambda x: x.find_element_by_xpath(self.close_membership_application_button))
        except Exception as e:
            return True
        else:
            logger.info('Succeed to close pop windows')
            return self._verify_and_click_element(self.close_membership_application_button)

    def play_music(self, wait_time=5):
        if not self.close_pop_window():
            return False
        logger.info('start to play music')
        if self.phone_info.phone_type == PhoneType.ANDROID:
            for i in range(10):
                try:
                    WebDriverWait(self.driver.appium_driver, wait_time, 1).until(
                        lambda x: x.find_element_by_xpath(self.pause_music_label))
                except Exception as e:
                    result = self._verify_and_click_element(self.play_music_label)
                    if result:
                        logger.info('Succeed to play music')
                        wait(3)
                    else:
                        logger.info('Fail to play music, try again')
                        wait(1)
                else:
                    logger.info('Music is playing')
                    return True
            else:
                return False
        else:
            logger.info('start to play music')
            for i in range(10):
                try:
                    ele_obj = self.driver.appium_driver.find_element_by_xpath(self.play_or_pause_music_button)
                    if ele_obj.text == "暂停":
                        return True
                    elif ele_obj.text == "播放":
                        result = self._verify_and_click_element(self.play_or_pause_music_button)
                        if result:
                            wait(1)
                            ele_obj = self.driver.appium_driver.find_element_by_xpath(self.play_or_pause_music_button)
                            if ele_obj.text == "暂停":
                                logger.info('Succeed to play music')
                                wait(3)
                                return True
                        else:
                            logger.info('Fail to play music, try again')
                            wait(1)
                    else:
                        wait(1)
                except Exception as e:
                    wait(1)
            else:
                return False

    def music_resuming_after_interruption(self, wait_time=5):
        logger.info('start to resume music')
        if self.phone_info.phone_type == PhoneType.ANDROID:
            for i in range(30):
                try:
                    WebDriverWait(self.driver.appium_driver, wait_time, 1).until(
                        lambda x: x.find_element_by_xpath(self.pause_music_label))
                except Exception as e:
                    logger.info('Music was not resumed, try again')
                    wait(1)
                else:
                    logger.info('Music has been resumed')
                    return True
            else:
                return False

        else:
            for i in range(30):
                try:
                    ele_obj = self.driver.appium_driver.find_element_by_xpath(self.play_or_pause_music_button)
                    if ele_obj.text == "暂停":
                        logger.info('Music has been resumed')
                        return True
                except Exception as e:
                    logger.info('Music was not resumed, try again')
                    wait(1)
            else:
                return False

    def pause_music(self, wait_time=5):
        logger.info('start to pause music')
        if self.phone_info.phone_type == PhoneType.ANDROID:
            for i in range(10):
                try:
                    WebDriverWait(self.driver.appium_driver, wait_time, 1).until(
                        lambda x: x.find_element_by_xpath(self.play_music_label))
                except Exception as e:
                    result = self._verify_and_click_element(self.pause_music_label)
                    if result:
                        logger.info('Succeed to pause music')
                        wait(1)
                    else:
                        logger.info('Fail to pause music, try again')
                        wait(1)
                else:
                    logger.info('Music has been paused')
                    return True
            else:
                return False
        else:
            for i in range(10):
                try:
                    ele_obj = self.driver.appium_driver.find_element_by_xpath(self.play_or_pause_music_button)
                    if ele_obj.text == "播放":
                        return True
                    elif ele_obj.text == "暂停":
                        result = self._verify_and_click_element(self.play_or_pause_music_button)
                        if result:
                            wait(1)
                            ele_obj = self.driver.appium_driver.find_element_by_xpath(self.play_or_pause_music_button)
                            if ele_obj.text == "播放":
                                logger.info('Succeed to pause music')
                                wait(3)
                                return True
                        else:
                            logger.info('Fail to pause music, try again')
                            wait(1)
                    else:
                        wait(1)
                except Exception as e:
                    wait(1)
            else:
                return False

    def no_reminder_for_music_interruption(self, wait_time=3):
        logger.info('Click no reminder button')
        try:
            WebDriverWait(self.driver.appium_driver, wait_time, 1).until(
                lambda x: x.find_element_by_xpath(self.music_interruption_no_reminder_button))
        except Exception as e:
            return True
        else:
            result = self._verify_and_click_element(self.music_interruption_no_reminder_button)
            if result:
                logger.info('Succeed to click no reminder button')
                return result
            else:
                logger.info('Fail to click no reminder button')
                return result

    def quit_app(self):
        logger.info('Quit QQ Music driver')
        try:
            self.driver.appium_driver.quit()
        except Exception as e:
            logger.error(e)
            logger.info('QQ Music driver cannot be quited')
            return False
        else:
            logger.info('QQ Music driver has been quited successfully')
            return True

    def close_app(self):
        logger.info('QQ Music will be closed')
        try:
            self.driver.appium_driver.close_app()
        except Exception as e:
            logger.error(e)
            logger.info('QQ Music cannot be closed')
            return False
        else:
            logger.info('QQ Music has been closed successfully')
            return True

    def activate_activity(self):
        logger.info('QQ Music app activity will be activate')
        try:
            self.driver.appium_driver.start_activity(self.package_name, self.activity_name)
        except Exception as e:
            logger.error(e)
            logger.info('QQ Music app activity cannot be activated')
            return False
        else:
            logger.info('QQ Music app activity has been activated')
            return True

    def activate_app(self):
        logger.info('QQ Music will be brought to foreground')
        try:
            self.driver.appium_driver.activate_app(self.package_name)
        except Exception as e:
            logger.error(e)
            logger.info('QQ Music cannot be brought to foreground')
            return False
        else:
            logger.info('QQ Music has been brought to foreground successfully')
            return True

    def terminate_app(self):
        logger.info('QQ Music will be terminated')
        try:
            self.driver.appium_driver.terminate_app(self.package_name)
        except Exception as e:
            logger.error(e)
            logger.info('QQ Music cannot be terminated')
            return False
        else:
            logger.info('QQ Music has been terminated successfully')
            return True

    def _verify_and_click_element(self, element, wait_time=5):
        """
        this is a common function used for verifying and clicking an element
        :param element: element by xpath
        :param wait_time: wait time and interval is 1s
        :return:
        """
        try:
            WebDriverWait(self.driver.appium_driver, wait_time, 1).until(lambda x: x.find_element_by_xpath(element))
        except Exception as e:
            logger.error(e)
            return False
        else:
            try:
                self.driver.appium_driver.find_element_by_xpath(element).click()
            except Exception as e:
                logger.error(e)
                return False
            else:
                return True