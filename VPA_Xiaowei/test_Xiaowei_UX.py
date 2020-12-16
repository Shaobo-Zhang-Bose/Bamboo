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
import threading
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
        def test_xiaowei_query(stepnum1 ,stepnum2):
            test_step(stepnum1, "Test xiaowei voice query for an hour", dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"

            test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            if query_item == "query_weather":
                assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
            else:
                assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_xiaowei_query(1, 2)

        time_end = datetime.datetime.now()
        run_time = (time_end - time_start).seconds
        left_time = 3600 - run_time
        logger.info('The test case has been running for %s seconds and there are %s seconds left' % (run_time, left_time))
        if run_time >= 3600:
            break
        else:
            wait(60)
    phone.xiaowei.swip_down(n=12)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Voice_Query_For_an_Hour_While_Music_Is_Streaming_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    time_start = datetime.datetime.now()
    test_step(1, "Launch QQ music", dut)
    assert phone.launch_application(PhoneAppType.QQMUSIC), "Failed to launch QQ music"
    test_step(2, "Play a music in QQ music", dut)
    assert phone.qqmusic.play_music(), "Failed to play music"
    assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "The QQ music was not played"
    test_step(3, "Re-launch xiaowei and Test xiaowei voice query a festival custom", dut)
    assert phone.xiaowei.activate_app(), "Failed to launch xiaowei"
    assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"

    while True:
        query_text = random.choice(list(query_response_dict["query_festival"]))
        response_text = query_response_dict["query_festival"][query_text]

        @retry(stop_max_attempt_number=3, wait_fixed=2000)
        def test_xiaowei_query(stepnum4 ,stepnum5 ,stepnum6):
            test_step(stepnum4, "Test xiaowei voice query for an hour", dut)
            XiaoweiSupport.test_vpa(dut, query_text, phone=phone)
            test_step(stepnum5, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
            assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
            assert XiaoweiSupport.test_a2dp_source(), "QQ music does not pause when vpa response is playing"
            test_step(stepnum6, "Re-launch xiaowei", dut)
            assert phone.xiaowei.activate_app(), "Failed to launch xiaowei"
            assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
        test_xiaowei_query(4, 5, 6)

        time_end = datetime.datetime.now()
        run_time = (time_end - time_start).seconds
        left_time = 3600 - run_time
        logger.info('The test case has been running for %s seconds and there are %s seconds left' % (run_time, left_time))
        if run_time >= 3600:
            break
        else:
            wait(60)
    test_step(7, "Close QQ music", dut)
    assert phone.qqmusic.terminate_app(), "Failed to close QQ music"
    wait(20)
    assert dut.status.get_sink_state() == SinkStates.CONNECTED, "Failed to close QQ music"

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Response_Conversation_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_conversation_interrupt(stepnum1):
        test_step(stepnum1, "Test xiaowei voice query the weather of a city", dut)
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
    test_conversation_interrupt(1)

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
    def test_cnc_interrupt(stepnum1):
        test_step(stepnum1, "Test xiaowei voice query the weather of a city", dut)
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

    test_cnc_interrupt(1)

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
    def test_xiaowei(stepnum2, stepnum3):
        test_step(stepnum2, "Test xiaowei voice query the weather", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(stepnum3, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_native(stepnum6):
        test_step(stepnum6, "Test native voice query the weather", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_native_vpa(), "native recording or streaming failed"
        assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to launch Xiaowei"

    for i in range(cycle):
        logger.info("Switch xiaoawei and native cycle for %d times, %d" % (cycle, i + 1))
        test_step(1, "Set VPA to Xiaowei", dut)
        assert dut.device.set_xiaowei_as_push_to_talk_vpa()
        test_xiaowei(2, 3)
        test_step(4, "Check Push to Talk status", dut)
        assert dut.status.get_push_to_talk_vpa_status() == '3'
        test_step(5, "Set VPA to Native", dut)
        assert dut.device.set_native_as_push_to_talk_vpa()
        test_native(6)
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

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def disconnect_dut_and_launch_xiaowei(stepnum1, stepnum2):
        test_step(stepnum1, "Disconnect dut", dut)
        assert phone.xiaowei.disconnect_device(), "Failed to disconnect dut"
        assert phone.xiaowei.close_app(), "Failed to close xiaowei"
        test_step(stepnum2, "Open xiaowei", dut)
        assert phone.xiaowei.launch_app(), "Failed to open Xiaowei"
        assert phone.xiaowei.verify_connection_prompt(), "Failed to verify connection prompt"
        assert phone.xiaowei.cancel_connection_prompt(), "Failed to cancel connection prompt"
        assert not phone.xiaowei.verify_device_icon(), "Dut cannot be connected with phone"
        assert phone.xiaowei.close_app(), "Failed to close xiaowei"
    disconnect_dut_and_launch_xiaowei(1,  2)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum3, stepnum4, stepnum5):
        test_step(stepnum3, "Re-Open xiaowei and Test voice query a weather of a city", dut)
        assert phone.xiaowei.launch_app(), "Failed to open Xiaowei"
        assert phone.xiaowei.verify_connection_prompt(), "Failed to verify connection prompt"
        assert phone.xiaowei.accept_connection_prompt(), "Failed to accept connection prompt"
        assert phone.xiaowei.verify_device_icon(), "Failed to connect with dut"

        query_response_dict = XiaoweiSupport.xw_query_response_dict()
        query_text = random.choice(list(query_response_dict["query_weather"]))
        response_text = query_response_dict["query_weather"][query_text]
        test_step(stepnum4, "Test xiaowei voice query the weather of a city", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(stepnum5, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
    test_xiaowei_query(3, 4, 5)
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
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query a story or a music", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_story_music(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text,  response_with_icon=True), "xiaowei query or response failed"
        wait(10)
    test_xiaowei_query(1, 2)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_decrease_volume(stepnum3):
        test_step(stepnum3, "Test xiaowei to decrease volume to min through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["decrease_volume"]
        result = False
        for i in range(20):
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
            if dut.status.get_volume() == min_volume:
                result = True
                break
        assert result, "Set volume to min failed"
    test_decrease_volume(3)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_increase_volume(stepnum4):
        test_step(stepnum4, "Test xiaowei to increase volume to max through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["increase_volume"]
        result = False
        for i in range(20):
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
            if dut.status.get_volume() == max_volume:
                result = True
                break
        assert result, "Set volume to max failed"
    test_increase_volume(4)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_other_control(stepnum5, stepnum6, stepnum7, stepnum8):
        test_step(stepnum5, "Test xiaowei to pause playing through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["pause_playing"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.CONNECTED, "pause streaming failed"

        test_step(stepnum6, "Test xiaowei to resume playing through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["resume_playing"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"

        test_step(stepnum7, "Test xiaowei to switch the next story or music through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["play_next"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"

        test_step(stepnum8, "Test xiaowei to switch the previous story or music through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["play_previous"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"
    test_other_control(5, 6, 7, 8)
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Control_Story_Music_After_Phone_Screen_Is_Locked_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    min_volume, max_volume = 0, 16
    lock_screen_time = 260
    control_story_or_music_dict = XiaoweiSupport.xw_control_story_or_music()
    query_text = random.choice(list(control_story_or_music_dict["story_music_dict"]))
    response_text = control_story_or_music_dict["story_music_dict"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query a story or a music", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_story_music(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text,  response_with_icon=True), "xiaowei query or response failed"
        wait(10)
    test_xiaowei_query(1, 2)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_decrease_volume(stepnum3):
        test_step(stepnum3, "Test xiaowei to decrease volume to min through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["decrease_volume"]
        result = False
        for i in range(20):
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
            if dut.status.get_volume() == min_volume:
                result = True
                break
        assert result, "Set volume to min failed"

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_increase_volume(stepnum4):
        test_step(stepnum4, "Test xiaowei to increase volume to max through vpa query", dut)
        query_text = control_story_or_music_dict["control_dict"]["increase_volume"]
        result = False
        for i in range(20):
            XiaoweiSupport.test_vpa(dut, query_text)
            assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
            if dut.status.get_volume() == max_volume:
                result = True
                break
        assert result, "Set volume to max failed"

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_other_control(stepnum5, stepnum6, stepnum7, stepnum8):
        test_step(stepnum5, "Test xiaowei voice query to pause stream", dut)
        query_text = control_story_or_music_dict["control_dict"]["pause_playing"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.CONNECTED, "pause streaming failed"

        test_step(stepnum6, "Test xiaowei voice query to resume streaming", dut)
        query_text = control_story_or_music_dict["control_dict"]["resume_playing"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"

        test_step(stepnum7, "Test xiaowei voice query to switch the next story or music", dut)
        query_text = control_story_or_music_dict["control_dict"]["play_next"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"

        test_step(stepnum8, "Test xiaowei voice query to switch the previous story or music", dut)
        query_text = control_story_or_music_dict["control_dict"]["play_previous"]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_query_no_response(), "xiaowei recording or streaming failed"
        wait(5)
        assert dut.status.get_sink_state() == SinkStates.A2DP_STREAMING, "resume streaming failed"

    condition = threading.Condition()

    def lock_screen(lock_time):
        with condition:
            phone.xiaowei.lock_screen(condition, lock_time)

    threading.Thread(target=lock_screen, args=(lock_screen_time,)).start()
    test_decrease_volume(3)
    test_increase_volume(4)
    test_other_control(5, 6, 7, 8)
    with condition:
        condition.notify()
        condition.wait()
    wait(2)
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
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query story or music and control volume to min or max through swipe captouch", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_story_music(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text,  response_with_icon=True), "xiaowei query or response failed"
        wait(5)
    test_xiaowei_query(1, 2)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_control_volume(stepnum3):
        test_step(stepnum3, "Test to control dut volume through double tap captouch", dut)
        assert XiaoweiSupport.test_swipe_up_down(), "failed to adjust volume to min or max"
        wait(5)
    test_control_volume(3)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_pause_and_resume_streaming(stepnum4):
        test_step(stepnum4, "Test to pause or resume streaming through double tap captouch", dut)
        assert XiaoweiSupport.test_double_tap(pause_streaming=True, resume_streaming=False), "failed to pause streaming"
        wait(5)
        assert XiaoweiSupport.test_double_tap(pause_streaming=False, resume_streaming=True), "failed to resume streaming"
    test_pause_and_resume_streaming(4)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_switch_streaming(stepnum5, stepnum6):
        test_step(stepnum5, "Test to switch the next story or music through swipe captouch forward", dut)
        assert XiaoweiSupport.test_swipe_forward_back(forward=True, back=False), "failed to switch next story or music"
        wait(5)
        test_step(stepnum6, "Test to switch the previous story or music through swipe captouch back", dut)
        assert XiaoweiSupport.test_swipe_forward_back(forward=False, back=True), "failed to switch previous story or music"
    test_switch_streaming(5, 6)
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
    wait(1)
    phone.bluetooth.bt_radio(enable='off')
    phone.bluetooth.bt_radio(enable='on')
    wait(1)
    assert phone.bluetooth.bt_connect(current_name), "Failed to connect to dut via bluetooth"
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

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2, stepnum3):
        for i in range(cycle):
            test_step(stepnum1, "Test xiaowei to voice query festival customs for %d times, %d" % (cycle, i+1), dut)
            XiaoweiSupport.test_vpa(dut, query_text)
            test_step(stepnum2, "Verify that swipe cap touch forward or back does not interrupt vpa response for %d times, %d" % (cycle, i+1), dut)
            assert XiaoweiSupport.test_swipe_forward_back(forward=True, back=True), "xiaowei recording or streaming failed"
        test_step(stepnum3, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query(1, 2, 3)

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

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Cancel_VPA_Query_Response_With_Double_Tap_Captouch_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_festival"]))
    response_text = query_response_dict["query_festival"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2, stepnum3):
        test_step(stepnum1, "Test xiaowei voice query a festival custom", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_step(stepnum3, "Test to cancel vpa response through double tap captouch", dut)
        assert XiaoweiSupport.test_double_tap(), "Failed to cancel vpa response"
    test_xiaowei_query(1, 2, 3)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_With_Long_Query_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["long_query"]))
    response_text = query_response_dict["long_query"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query with a long query", dut)
        XiaoweiSupport.test_vpa(dut, query_text, hold_seconds=12)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query(1, 2)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Phone_Lose_Network_When_Xiaowei_Query_Is_In_Progress_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_festival"]))
    response_text = query_response_dict["query_festival"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query_without_network(stepnum1):
        test_step(stepnum1, "Turn off network when Test xiaowei voice query a festival custom", dut)
        assert XiaoweiSupport.test_vpa(dut, query_text, hold_seconds=12, phone=phone, turn_off_network=True), "xiaowei query or response failed"
        wait(2)
        assert XiaoweiSupport.test_xiaowei_vpa(), "No local prompts streaming"
    test_xiaowei_query_without_network(1)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum2, stepnum3):
        test_step(stepnum2, "Turn on network", dut)
        assert phone.launch_application(PhoneAppType.SETTINGS), "Failed to launch settings"
        assert phone.settings.cellular_on(), "Failed to turn on cellular"
        assert phone.settings.wifi_on(), "Failed to turn on wifi"
        test_step(stepnum3, "Re-launch xiaowei and Test xiaowei voice query a festival custom", dut)
        assert phone.xiaowei.activate_app(), "Failed to launch xiaowei"
        assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query(2, 3)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Disable_Phone_Bluetooth_When_Xiaowei_Query_Is_In_Progress_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    current_name = dut.bluetooth.get_name()
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_festival"]))
    response_text = query_response_dict["query_festival"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query_without_bluetooth(stepnum1):
        test_step(stepnum1, "Disable bluetooth when test xiaowei voice query a festival custom", dut)
        assert XiaoweiSupport.test_vpa(dut, query_text, hold_seconds=12, phone=phone, turn_off_bluetooth=True), "xiaowei query or response failed"
        wait(2)
        assert XiaoweiSupport.get_current_dut_sink_state() == SinkStates.ANR_ONLY, "The sink state was wrong"
    test_xiaowei_query_without_bluetooth(1)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum2, stepnum3):
        test_step(stepnum2, "Launch Bluetooth and Enable bluetooth", dut)
        assert phone.launch_application(PhoneAppType.BLUETOOTH), "Failed to launch bluetooth"
        assert phone.bluetooth.bt_radio(enable='on'), "Failed to enable bluetooth"
        wait(5)
        if not phone.bluetooth.bt_is_connected_to(current_name):
            assert phone.bluetooth.connect_paired_device(current_name), "Failed to connect to dut via bluetooth"
        wait(1)
        test_step(stepnum3, "Re-launch xiaowei and Test xiaowei voice query a festival custom", dut)
        assert phone.xiaowei.activate_app(), "Failed to launch xiaowei"
        assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query(2, 3)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Close_Xiaowei_When_Xiaowei_Query_Is_In_Progress_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_festival"]))
    response_text = query_response_dict["query_festival"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query a festival custom", dut)
        assert XiaoweiSupport.test_vpa(dut, query_text, hold_seconds=12, phone=phone, close_xiaowei=True), "xiaowei query or response failed"
        assert XiaoweiSupport.get_current_dut_sink_state() == SinkStates.CONNECTED, "The sink state was wrong"
        test_step(stepnum2, "Launch xiaowei and Test xiaowei voice query a festival custom", dut)
        assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to launch xiaowei"
        wait(5)
        assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query(1, 2)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_While_Xiaowei_Is_In_Translation_Mode_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    wait(3)
    translation_mode = XiaoweiSupport.xw_in_translation_mode()

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2, stepnum3):
        query_text = list(translation_mode["goto_translation_mode"].keys())[0]
        response_text = list(translation_mode["goto_translation_mode"].values())[0]
        test_step(stepnum1, "Test xiaowei go to translation mode", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_step(stepnum2, "Test voice query translation by xiaowei", dut)
        query_text = list(translation_mode["translation_sentence"].keys())[0]
        response_text = list(translation_mode["translation_sentence"].values())[0]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
        test_step(stepnum3, "Test xiaowei quit translation mode", dut)
        query_text = list(translation_mode["quit_translation_mode"].keys())[0]
        response_text = list(translation_mode["quit_translation_mode"].values())[0]
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query(1, 2, 3)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_While_Phone_IS_In_Airplane_Mode_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    current_name = dut.bluetooth.get_name()
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_festival"]))
    response_text = query_response_dict["query_festival"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def turn_on_airplane_mode(stepnum1):
        test_step(stepnum1, "Turn on airplane mode", dut)
        assert phone.launch_application(PhoneAppType.SETTINGS), "Failed to launch settings"
        assert phone.settings.airplane_on(), "Failed to turn on airplane mode"
        assert phone.settings.cellular_off(), "Failed to turn off cellular"
        assert phone.settings.wifi_off(), "Failed to turn off wifi"
        assert phone.settings.terminate_app(), "Failed to terminate settings"
    turn_on_airplane_mode(1)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def turn_on_bluetooth(stepnum2):
        test_step(stepnum2, "Launch Bluetooth and turn on bluetooth", dut)
        assert phone.launch_application(PhoneAppType.BLUETOOTH), "Failed to launch bluetooth"
        assert phone.bluetooth.bt_radio(enable='on'), "Failed to enable bluetooth"
        wait(5)
        if not phone.bluetooth.bt_is_connected_to(current_name):
            assert phone.bluetooth.connect_paired_device(current_name), "Failed to connect to dut via bluetooth"
        wait(1)
        assert phone.launch_application(PhoneAppType.SETTINGS), "Failed to launch bluetooth"
        assert phone.settings.terminate_app(), "Failed to terminate settings"
    turn_on_bluetooth(2)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query_in_airplane_mode(stepnum3):
        test_step(stepnum3, "Launch xiaowei and Test xiaowei voice query a festival custom", dut)
        assert phone.xiaowei.activate_app(), "Failed to launch xiaowei"
        XiaoweiSupport.test_vpa(dut, query_text), "xiaowei query or response failed"
        assert XiaoweiSupport.test_xiaowei_vpa(), "No local prompt streaming"
    test_xiaowei_query_in_airplane_mode(3)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def turn_off_airplane_mode(stepnum4):
        test_step(stepnum4, "Turn off airplane and turn on network", dut)
        assert phone.launch_application(PhoneAppType.SETTINGS), "Failed to launch settings"
        assert phone.settings.airplane_off(), "Failed to turn off airplane"
        assert phone.settings.cellular_on(), "Failed to turn on cellular"
        assert phone.settings.wifi_on(), "Failed to turn on wifi"
        wait(5)
    turn_off_airplane_mode(4)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum5):
        test_step(stepnum5, "Re-launch xiaowei and Test xiaowei voice query a festival custom", dut)
        assert phone.xiaowei.activate_app(), "Failed to launch xiaowei"
        assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query(5)
    
@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Voice_Prompts_While_Voice_Prompts_Is_Disabled_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    wait(3)
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_festival"]))
    response_text = query_response_dict["query_festival"][query_text]

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query_without_network(stepnum1, stepnum2):
        test_step(stepnum1, "Turn off network", dut)
        assert phone.launch_application(PhoneAppType.SETTINGS), "Failed to launch settings"
        assert phone.settings.cellular_off(), "Failed to turn off cellular"
        assert phone.settings.wifi_off(), "Failed to turn off wifi"
        test_step(stepnum2, "Re-launch xiaowei and Test voice query a festival customs", dut)
        assert phone.xiaowei.activate_app(), "Failed to launch xiaowei"
        assert XiaoweiSupport.test_vpa(dut, query_text), "xiaowei query or response failed"
        assert XiaoweiSupport.test_xiaowei_vpa(), "No local prompt streaming"
    test_xiaowei_query_without_network(1, 2)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query_with_disable_voice_prompt(stepnum3, stepnum4):
        test_step(stepnum3, "Disable voice prompts", dut)
        dut.status.disable_voice_prompt()
        wait(2)
        assert not dut.status.is_voice_prompt_enabled(), "Failed to disable voice prompts."
        test_step(stepnum4, "Test xiaowei voice query a festival customs", dut)
        assert XiaoweiSupport.test_vpa(dut, query_text), "xiaowei query or response failed"
        assert XiaoweiSupport.test_xiaowei_vpa(), "No local prompt streaming"
    test_xiaowei_query_with_disable_voice_prompt(3, 4)

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query_with_enable_voice_prompt(stepnum5, stepnum6, stepnum7):
        test_step(stepnum5, "Enable voice prompts", dut)
        dut.status.enable_voice_prompt()
        wait(2)
        assert dut.status.is_voice_prompt_enabled(), "Failed to enable voice prompts."
        test_step(stepnum6, "Turn on network", dut)
        assert phone.settings.activate_app(), "Failed to launch settings"
        assert phone.settings.cellular_on(), "Failed to turn on cellular"
        assert phone.settings.wifi_on(), "Failed to turn on wifi"
        test_step(7, "Re-launch xiaowei and Test xiaowei voice query a festival custom", dut)
        assert phone.xiaowei.activate_app(), "Failed to launch xiaowei"
        assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    test_xiaowei_query_with_enable_voice_prompt(5, 6, 7)
