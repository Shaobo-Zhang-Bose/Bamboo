#!/usr/bin/python
# -*- coding  utf-8 -*-
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
Test Case ID : Xiaowei_UX
Description  : Xiaowei UX for audio query
Pre-condition: Xiaowei UX-Standby
"""
from wham_automation.JiraKnownIssues import KnownIssue

__docformat__ = 'restructuredtext en'
__author__ = 'Shaobo Zhang'

import pytest
import os
import random
import datetime
from retrying import retry
from wham_automation.lib.framework.Configs.ProductInfo import ProductFeature, Buttons
from wham_automation.lib.mobile.scenario.PhoneObject import PhoneType
from wham_automation.script_support.AssertHelpers import SinkStates
from wham_automation.script_support.CommonFixture import ScriptCommon
from wham_automation.script_support.FilterDecorators import TestFilters
from wham_automation.script_support.ScriptHelper import test_step, wait
from wham_automation.test_scripts.LEDMapping import LEDState
from wham_automation.test_scripts.ToneStatusMapping import ToneState
from wham_automation.test_scripts.VoiceStateMapping import VoiceState
from wham_automation.script_support.CommonFixture import PhoneAppType
from wham_automation.utils.log import logger
from wham_automation.test_scripts.Bamboo.VPA_Xiaowei.Xiaowei_Support import XiaoweiSupport, VPAProcess, GenerateVoiceToQuery
from wham_automation.script_support import Precondition

@pytest.fixture(scope='function')
def automation_xiaowei_ux(dut_precondition_connected_activated_in_xiaowei):
    logger.info('--------------starting test case setup---------------')
    assert dut_precondition_connected_activated_in_xiaowei, "Failed to connect to dut through bluetooth"
    dut = dut_precondition_connected_activated_in_xiaowei.dut_list[0]
    phone = dut_precondition_connected_activated_in_xiaowei.phones[0]
    assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed while going to launch Xiaowei"
    assert phone.xiaowei.insure_device_connection(), "Failed to connect to dut"

    yield dut, phone

    logger.info('--------------starting test case cleanup---------------')
    assert phone.xiaowei.disconnect_device(), "Failed to disconnect dut from xiaowei"
    assert phone.xiaowei.quit(), "Failed to close xiaowei"
    phone._set_current_app_to_none()

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Show_Different_Device_Name_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    original_device_name = dut.bluetooth.get_name()
    logger.info("Current device name: %s" % original_device_name)
    test_step(1, "Check original device name in xiaowei APP", dut)
    assert phone.xiaowei.verify_device_name(original_device_name), "Wrong device name was displayed in xiaowei"
    new_device_name = "QWERtyuiopasdfghjklzxcvbnm"
    dut.bluetooth.set_name(new_device_name)
    test_step(2, "Set new device name", dut)
    assert new_device_name == dut.bluetooth.get_name(), "Failed to set new device name"
    logger.info("Device name was successfully set to %s" % new_device_name)
    test_step(3, "Close xiaowei APP", dut)
    assert phone.xiaowei.close_app(), "Failed to close Xiaowei"
    test_step(4, "Re-open xiaowei APP", dut)
    assert phone.xiaowei.launch_app(), "Failed while going to open Xiaowei"
    test_step(5, "Check new device name in xiaowei APP", dut)
    assert phone.xiaowei.verify_device_name(new_device_name), "Wrong device name was displayed in xiaowei"
    logger.info("Restore device name to original name: %s" % original_device_name)
    dut.bluetooth.set_name(original_device_name)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Voice_Query_Weekday_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weekday"]))
    response_text = query_response_dict["query_weekday"][query_text]
    test_step(1, "Test xiaowei voice query the day of the week", dut)
    XiaoweiSupport.test_vpa(dut, query_text)
    assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"

    test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
    assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Voice_Query_Weather_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]
    test_step(1, "Test xiaowei voice query the weather of a city", dut)
    XiaoweiSupport.test_vpa(dut, query_text)
    assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"

    test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
    assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Voice_Query_Weather_Cycle_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    cycle = 10
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_weather_cycle = list(query_response_dict["query_weather"])
    for i in range(cycle):
        query_text = random.choice(query_weather_cycle)
        response_text = query_response_dict["query_weather"][query_text]

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def retest():
            test_step(1, "Test xiaowei voice query the weather in different cities for %d times, %d" % (cycle, i+1), dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"

            test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
        retest()
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Ping_Pong_Voice_Query_Cycle_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    cycle = 10
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_weekday_cycle = list(query_response_dict["query_weekday"])
    query_weather_cycle = list(query_response_dict["query_weather"])
    for i in range(cycle):
        query_text = random.choice(query_weekday_cycle)
        response_text = query_response_dict["query_weekday"][query_text]

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def test_xiaowei_query():
            test_step(1, "Test xiaowei ping pong voice query for %d times, %d" % (cycle, i+1), dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"

            test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_xiaowei_query()

        query_text = random.choice(query_weather_cycle)
        response_text = query_response_dict["query_weather"][query_text]

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def test_pingpong_query():
            test_step(3, "Test xiaowei ping pong voice query for %d times, %d" % (cycle, i+1), dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"

            test_step(4, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
        test_pingpong_query()
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Interrupt_Response_By_New_Voice_Query_Cycle_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    cycle = 10
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_weather_cycle = list(query_response_dict["query_weather"])
    query_festival_cycle = list(query_response_dict["query_festival"])
    for i in range(cycle):
        query_text = random.choice(query_weather_cycle)
        response_text = query_response_dict["query_weather"][query_text]

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def test_xiaowei_query():
            test_step(1, "Test xiaowei to interrupt the last response for %d times, %d" % (cycle, i+1), dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_interruption(), "xiaowei recording or streaming failed"

            test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
        test_xiaowei_query()

        query_text = random.choice(query_festival_cycle)
        response_text = query_response_dict["query_festival"][query_text]

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def test_interrupt_response():
            test_step(3, "Test xiaowei to interrupt the last response for %d times, %d" % (cycle, i+1), dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_interruption(), "xiaowei recording or streaming failed"

            test_step(4, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_interrupt_response()
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Disconnect_Connect_HP_and_Query_Cycle_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    cycle = 20
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_weather_cycle = list(query_response_dict["query_weather"])
    wait(20)
    for i in range(cycle):
        test_step(1, "Test xiaowei Disconnect and Connect HP then conduct voice query for %d times, %d" % (cycle, i+1), dut)
        test_step(1, "Disconnect dut", dut)
        assert phone.xiaowei.disconnect_device(), "Failed to disconnect dut"
        test_step(2, "Close xiaowei APP", dut)
        assert phone.xiaowei.close_app(), "Failed to close xiaowei"
        test_step(3, "Re-open xiaowei APP", dut)
        assert phone.xiaowei.launch_app(), "Failed to re-open Xiaowei"
        test_step(4, "Verify prompt and accept it", dut)
        assert phone.xiaowei.verify_connection_prompt(), "Failed to verify connection prompt"
        assert phone.xiaowei.accept_connection_prompt(), "Failed to accept connection prompt"
        test_step(5, "Verify if xiaowei connect to dut", dut)
        assert phone.xiaowei.verify_device_icon(), "Failed to connect with dut"

        query_text = random.choice(query_weather_cycle)
        response_text = query_response_dict["query_weather"][query_text]

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def test_xiaowei_query():
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"

            test_step(6, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
        test_xiaowei_query()
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Voice_Query_For_an_Hour_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_weekday_cycle = list(query_response_dict["query_weekday"])
    query_weather_cycle = list(query_response_dict["query_weather"])
    query_festival_cycle = list(query_response_dict["query_festival"])

    query_list = list()
    query_list.extend(query_weekday_cycle)
    query_list.extend(query_weather_cycle)
    query_list.extend(query_festival_cycle)

    time_start = datetime.datetime.now()
    wait(60)

    while True:
        query_text = random.choice(query_list)
        for query_item in (["query_weekday", "query_weather", "query_festival"]):
            response_text = query_response_dict[query_item].get(query_text)
            if response_text is not None:
                break
        logger.info('The query text is %s,  the corresponding response is %s' % (query_text, response_text))

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def test_xiaowei_query():
            test_step(1, "Test xiaowei voice query for an hour", dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"

            test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            if query_item == "query_weather":
                assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
            else:
                assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_xiaowei_query()

        time_end = datetime.datetime.now()
        run_time = (time_end - time_start).seconds
        left_time = 3600 - run_time
        logger.info('The test case has been running for %s seconds and there are %s seconds left' % (run_time, left_time))
        wait(60)
        if run_time >= 3600:
            break
    phone.xiaowei.swip_down(n=12)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Response_Conversation_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_conversation_interrupt():
        test_step(1, "Test xiaowei voice query the weather of a city", dut)
        control_dut_button_gesture = VPAProcess(dut=dut, button=Buttons.VPA, hold_seconds=5, how_many_times=1)
        control_dut_button_gesture.start()
        voice_to_query = GenerateVoiceToQuery(query_text)
        voice_to_query.play_query_voice()
        control_dut_button_gesture.join()
        count = 0
        while count < 20:
            logger.info("Check if the ss has changed to A2DP_STREAMING")
            if dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
                logger.info("Response is playing")
                break
            else:
                wait(0.5)
                count += 1
        dut.manager.cnc_tap_hold(hold_seconds=2, how_many_times=1)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING
        assert not dut.status.is_conversion_mode_enabled()
        assert phone.xiaowei.verify_query_response_text(query_text, response_text,
                                                        response_with_icon=True), "xiaowei query or response failed"
    test_conversation_interrupt()

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Response_CNC_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    current_cnc = dut.status.get_cnc_level()
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_cnc_interrupt():
        test_step(1, "Test xiaowei voice query the weather of a city", dut)
        control_dut_button_gesture = VPAProcess(dut=dut, button=Buttons.VPA, hold_seconds=5, how_many_times=1)
        control_dut_button_gesture.start()
        voice_to_query = GenerateVoiceToQuery(query_text)
        voice_to_query.play_query_voice()
        control_dut_button_gesture.join()
        count = 0
        while count < 20:
            logger.info("Check if the ss has changed to A2DP_STREAMING")
            if dut.status.get_sink_state() == SinkStates.A2DP_STREAMING:
                logger.info("Response is playing")
                break
            else:
                wait(0.5)
                count += 1
        dut.manager.cnc_tap_hold()
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING
        assert dut.status.get_cnc_level() != current_cnc
        assert phone.xiaowei.verify_query_response_text(query_text, response_text,
                                                        response_with_icon=True), "xiaowei query or response failed"

    test_cnc_interrupt()

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Native_Switch_Cycle_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]
    wait(2)
    cycle = 20

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei():
        test_step(2, "Test xiaowei voice query the weather", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(3, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_native():
        test_step(6, "Test native voice query the weather", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_native_vpa(), "native recording or streaming failed"
        assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to launch Xiaowei"

    for i in range(cycle):
        logger.info("Switch xiaoawei and native cycle for %d times, %d" % (cycle, i + 1))
        test_step(1, "Set VPA to Xiaowei", dut)
        assert dut.device.set_xiaowei_as_push_to_talk_vpa()
        test_xiaowei()
        test_step(4, "Check Push to Talk status", dut)
        assert dut.status.get_push_to_talk_vpa_status() == '3'
        test_step(5, "Set VPA to Native", dut)
        assert dut.device.set_native_as_push_to_talk_vpa()
        test_native()
        test_step(7, "Check Push to Talk status", dut)
        assert dut.status.get_push_to_talk_vpa_status() == '2'
        wait(1)

    test_step(8, "Set VPA to Xiaowei", dut)
    assert dut.device.set_xiaowei_as_push_to_talk_vpa()
    wait(2)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Cancel_Prompt_Request_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    test_step(1, "Disconnect dut", dut)
    assert phone.xiaowei.disconnect_device(), "Failed to disconnect dut"
    assert phone.xiaowei.close_app(), "Failed to close xiaowei"
    test_step(2, "Open xiaowei", dut)
    assert phone.xiaowei.launch_app(), "Failed to open Xiaowei"
    test_step(3, "Verify prompt and accept it", dut)
    assert phone.xiaowei.verify_connection_prompt(), "Failed to verify connection prompt"
    assert phone.xiaowei.cancel_connection_prompt(), "Failed to cancel connection prompt"
    test_step(4, "Verify if xiaowei connect to dut", dut)
    assert not phone.xiaowei.verify_device_icon(), "Dut cannot be connected with phone"
    assert phone.xiaowei.close_app(), "Failed to close xiaowei"
    test_step(5, "Re-Open xiaowei", dut)
    assert phone.xiaowei.launch_app(), "Failed to open Xiaowei"
    test_step(6, "Verify prompt and accept it", dut)
    assert phone.xiaowei.verify_connection_prompt(), "Failed to verify connection prompt"
    assert phone.xiaowei.accept_connection_prompt(), "Failed to accept connection prompt"
    test_step(7, "Verify if xiaowei connect to dut", dut)
    assert phone.xiaowei.verify_device_icon(), "Failed to connect with dut"

    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]
    test_step(8, "Test xiaowei voice query the weather of a city", dut)
    XiaoweiSupport.test_vpa(dut, query_text)
    assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
    test_step(9, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
    assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Control_Story_Music_Playing_Through_VPA_Query_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    min_volume, max_volume = 0, 16
    control_story_or_music_dict = XiaoweiSupport.xw_control_story_or_music()
    query_text = random.choice(list(control_story_or_music_dict["story_music_dict"]))
    response_text = control_story_or_music_dict["story_music_dict"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query():
        test_step(1, "Test xiaowei voice query a story or a music", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_story_music(), "xiaowei recording or streaming failed"
        test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text,  response_with_icon=True), "xiaowei query or response failed"
        wait(10)
    test_xiaowei_query()

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_decrease_volume():
        test_step(3, "Test xiaowei to decrease volume to min through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["decrease_volume"]
        result = False
        for i in range(20):
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"

            if dut.status.get_volume() == min_volume:
                result = True
                break
        assert result, "Set volume to min failed"
    test_decrease_volume()

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_increase_volume():
        test_step(4, "Test xiaowei to increase volume to max through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["increase_volume"]
        result = False
        for i in range(20):
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"

            if dut.status.get_volume() == max_volume:
                result = True
                break
        assert result, "Set volume to max failed"
    test_increase_volume()

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_other_control():
        test_step(5, "Test xiaowei to pause playing through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["pause_playing"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.CONNECTED, "pause streaming failed"

        test_step(6, "Test xiaowei to resume playing through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["resume_playing"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"

        test_step(7, "Test xiaowei to switch the next story or music through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["play_next"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"

        test_step(8, "Test xiaowei to switch the previous story or music through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["play_previous"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"
    test_other_control()
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Control_Story_Music_Playing_Through_Cap_Touch_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    control_story_or_music_dict = XiaoweiSupport.xw_control_story_or_music()
    query_text = random.choice(list(control_story_or_music_dict["story_music_dict"]))
    response_text = control_story_or_music_dict["story_music_dict"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query():
        test_step(1, "Test xiaowei voice query story or music and control volume to min or max through swipe captouch", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_story_music(), "xiaowei recording or streaming failed"
        test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text,  response_with_icon=True), "xiaowei query or response failed"
        wait(5)
    test_xiaowei_query()

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_control_volume():
        test_step(3, "Test to control dut volume through double tap captouch", dut)
        assert XiaoweiSupport.test_swipe_up_down(), "failed to adjust volume to min or max"
        wait(5)
    test_control_volume()

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_pause_and_resume_streaming():
        test_step(4, "Test to pause or resume streaming through double tap captouch", dut)
        assert XiaoweiSupport.test_double_tap(pause_streaming=True, resume_streaming=False), "failed to pause streaming"
        wait(5)
        assert XiaoweiSupport.test_double_tap(pause_streaming=False, resume_streaming=True), "failed to resume streaming"
    test_pause_and_resume_streaming()

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_switch_streaming():
        test_step(5, "Test to switch the next story or music through swipe captouch forward", dut)
        assert XiaoweiSupport.test_swipe_forward_back(forward=True, back=False), "failed to switch next story or music"
        wait(5)
        test_step(6, "Test to switch the previous story or music through swipe captouch back", dut)
        assert XiaoweiSupport.test_swipe_forward_back(forward=False, back=True), "failed to switch previous story or music"
    test_switch_streaming()
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Control_VPA_Response_Volume_Through_Captouch_Cycle_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    cycle = 5
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_festival_cycle = list(query_response_dict["query_festival"])
    for i in range(cycle):
        query_text = random.choice(query_festival_cycle)
        response_text = query_response_dict["query_festival"][query_text]

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def test_xiaowei_query():
            test_step(1, "Test xiaowei voice query a festival customs and control response volume by swipe captouch for %d times, %d"  % (cycle, i + 1), dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_swipe_up_down(), "xiaowei recording or streaming failed"
            test_step(2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_xiaowei_query()
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Reconection_After_Clearing_PDL_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    current_name = dut.bluetooth.get_name()
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query the weather of a city", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
    test_xiaowei_query(1, 2)
    test_step(3, "Perform clear PDL for dut", dut)
    dut.bluetooth.perform_clear_list()
    assert not phone.xiaowei.verify_device_icon(), "Failed to clear PDL"
    # phone.xiaowei.close_app() this step may cause launch next app failed
    test_step(4, "Reconnect dut via bluetooth", dut)
    phone.launch_application(PhoneAppType.BLUETOOTH)
    wait(2)
    for device in phone.bluetooth.bt_get_pairlist():
        phone.bluetooth.bt_unpair(device)
    dut.bluetooth.set_discoverable()
    phone.bluetooth.bt_radio(enable='off')
    phone.bluetooth.bt_radio(enable='on')
    assert phone.bluetooth.bt_connect(current_name), "Failed to reconnect dut via bluetooth"
    # phone.bluetooth.close_app() this step may cause launch next app failed
    test_step(5, "Switch to xiaowei APP", dut)
    assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to switch to Xiaowei"
    test_step(6, "Verify if xiaowei connect to dut", dut)
    assert phone.xiaowei.verify_device_icon(), "Failed to connect dut via xiaowei"
    test_xiaowei_query(7, 8)
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_VPA_Status_After_Factory_Default_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    current_name = dut.bluetooth.get_name()
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query the weather of a city", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
    test_xiaowei_query(1, 2)
    test_step(3, "Perform factory default", dut)
    assert dut.device.perform_factory_default(restore_name=True, wait_time_after_fd=5), "Failed to perform factory default"
    assert dut.device.perform_system_reset(), "Failed to perform factory default"
    dut.manager.initialize()
    test_step(4, "Check PPT of native VPA", dut)
    assert dut.status.get_push_to_talk_vpa_status() == '2', "Failed to check PTT status of native VPA"
    # phone.xiaowei.close_app() this step may cause launch next app failed
    test_step(5, "Reconnect dut via bluetooth", dut)
    phone.launch_application(PhoneAppType.BLUETOOTH)
    for device in phone.bluetooth.bt_get_pairlist():
        phone.bluetooth.bt_unpair(device)
    dut.bluetooth.set_discoverable()
    phone.bluetooth.bt_radio(enable='off')
    phone.bluetooth.bt_radio(enable='on')
    assert phone.bluetooth.bt_connect(current_name), "Failed to reconnect dut via bluetooth"
    # phone.bluetooth.close_app() this step may cause launch next app failed
    test_step(6, "Switch to xiaowei APP", dut)
    assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to switch to Xiaowei"
    test_step(7, "Verify if xiaowei connect to dut", dut)
    assert phone.xiaowei.insure_device_connection(), "Failed to connect dut via xiaowei"
    test_xiaowei_query(8, 9)
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Query_Response_With_Unsupported_Captouch_Gestures(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    cycle = 5
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_festival"]))
    response_text = query_response_dict["query_festival"][query_text]
    for i in range(cycle):
        test_step(1, "Test xiaowei to voice query festival customs for %d times, %d" % (cycle, i+1), dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        test_step(2, "Verify that swipe cap touch forward or back does not interrupt vpa response for %d times, %d" % (cycle, i+1), dut)
        assert XiaoweiSupport.test_swipe_forward_back(forward=True, back=True), "xiaowei recording or streaming failed"

    test_step(3, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
    assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_While_HP_Is_In_Discoverable_State_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    current_name = dut.bluetooth.get_name()
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_festival"]))
    response_text = query_response_dict["query_festival"][query_text]
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query a festival customs", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query(1, 2)
    dut.bluetooth.set_discoverable()
    assert dut.status.is_pairing_mode_enabled(), "dut is not in discoverable state"
    if dut.manager.multi_connection_supprot():
        test_step(3, "Test xiaowei voice query a festival customs", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_discoverable_state(), "xiaowei recording or streaming failed"
        test_step(4, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_step(5, "Reconnect dut via bluetooth", dut)
    # phone.xiaowei.close_app() this step may cause launch next app failed
    phone.launch_application(PhoneAppType.BLUETOOTH)
    for device in phone.bluetooth.bt_get_pairlist():
        phone.bluetooth.bt_unpair(device)
    #Dut is in pair mode for a long time, it may connect LE firstly, so set it to pair mode again.
    dut.bluetooth.set_discoverable()
    phone.bluetooth.bt_radio(enable='off')
    phone.bluetooth.bt_radio(enable='on')
    assert phone.bluetooth.bt_connect(current_name), "Failed to reconnect dut via bluetooth"
    # phone.bluetooth.close_app() this step may cause launch next app failed
    test_step(6, "Switch to xiaowei APP", dut)
    assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to switch to Xiaowei"
    test_step(7, "Verify if xiaowei connect to dut", dut)
    assert phone.xiaowei.insure_device_connection(), "Failed to connect dut via xiaowei"
    test_xiaowei_query(8, 9)
    phone.xiaowei.swip_down(n=8)

