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
Test Case ID : Xiaowei_Connect
Description  : Xiaowei basic connection
Pre-condition: Connected-Standby
"""
from wham_automation.JiraKnownIssues import KnownIssue

__docformat__ = 'restructuredtext en'
__author__ = 'Shaobo Zhang'

import pytest
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
import random
import time
from retrying import retry

@pytest.fixture(scope='function')
def automation_xiaowei_connect(dut_precondition_connected_activated_in_xiaowei):
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
def test_Xiaowei_Accept_Prompt_01(automation_xiaowei_connect):
    dut = automation_xiaowei_connect[0]
    phone = automation_xiaowei_connect[1]
    test_step(1, "Disconnect dut", dut)
    assert phone.xiaowei.disconnect_device(), "Failed to disconnect dut"
    assert phone.xiaowei.close_app(), "Failed to close xiaowei"
    test_step(2, "Open xiaowei", dut)
    assert phone.xiaowei.launch_app(), "Failed to open Xiaowei"
    test_step(3, "Verify prompt and accept it", dut)
    assert phone.xiaowei.verify_connection_prompt(), "Failed to verify connection prompt"
    assert phone.xiaowei.accept_connection_prompt(), "Failed to accept connection prompt"
    test_step(4, "Verify if xiaowei connect to dut", dut)
    assert phone.xiaowei.verify_device_icon(), "Failed to connect with dut"

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Reopen_Cycle_01(automation_xiaowei_connect):
    dut = automation_xiaowei_connect[0]
    phone = automation_xiaowei_connect[1]
    assert phone.xiaowei.verify_device_icon(), "Failed to connect with dut"
    cycle = 20
    for i in range(cycle):
        logger.info("Test xiaowei reopen for %d times, %d" % (cycle, i+1))
        test_step(1, "Close xiaowei APP", dut)
        assert phone.xiaowei.close_app(), "Failed to close xiaowei"
        test_step(2, "Re-open xiaowei APP", dut)
        assert phone.xiaowei.launch_app(), "Failed to re-open Xiaowei"
        test_step(3, "Verify if xiaowei connect to dut", dut)
        assert phone.xiaowei.verify_device_icon(), "Failed to connect with dut"

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Disconnect_Cycle_01(automation_xiaowei_connect):
    dut = automation_xiaowei_connect[0]
    phone = automation_xiaowei_connect[1]
    assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
    cycle = 20
    for i in range(cycle):
        logger.info("Test disconnect xiaowei and reopen for %d times, %d" % (cycle, i + 1))
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

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Dut_Power_Cycle_01(automation_xiaowei_connect):
    dut = automation_xiaowei_connect[0]
    phone = automation_xiaowei_connect[1]
    assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
    cycle = 20
    for i in range(cycle):
        logger.info("Power cycle dut for %d times, %d" % (cycle, i + 1))
        test_step(1, "Power off dut", dut)
        dut.key.press_power_off()
        test_step(2, "Verify if xiaowei connect to dut", dut)
        assert not phone.xiaowei.verify_device_icon(wait_time=3), "Xiaowei still connect"
        test_step(3, "Power on dut", dut)
        dut.key.press_power_on()
        test_step(4, "Verify if xiaowei connect to dut", dut)
        assert phone.xiaowei.verify_device_icon(), "Fail to connect with dut"

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Bluetooth_Disable_Cycle_01(automation_xiaowei_connect):
    dut = automation_xiaowei_connect[0]
    current_name = dut.bluetooth.get_name()
    phone = automation_xiaowei_connect[1]
    assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
    cycle = 20
    for i in range(cycle):
        logger.info("Test Bluetooth disable and enable cycle for %d times, %d" % (cycle, i + 1))
        test_step(1, "Switch to bluetooth settings", dut)
        assert phone.launch_application(PhoneAppType.BLUETOOTH), "Failed to switch to bluetooth settings"
        test_step(2, "Disable bluetooth on phone", dut)
        assert phone.bluetooth.bt_radio(enable='off'), "Failed to disable bluetooth"
        test_step(3, "Enable bluetooth on phone", dut)
        assert phone.bluetooth.bt_radio(enable='on'), "Failed to enable bluetooth"
        # iPhone will not connect with blutooth device after disable/enable bluetooth
        wait(3)
        if not phone.bluetooth.bt_is_connected_to(current_name):
            assert phone.bluetooth.connect_paired_device(current_name), "Failed to dut via bluetooth"
        wait(0.5) ###iap issue workaround
        test_step(4, "Switch to xiaowei APP", dut)
        assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to switch to Xiaowei"
        test_step(5, "Verify if xiaowei connect to dut", dut)
        assert phone.xiaowei.verify_device_icon(), "Fail to connect with dut"

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Hibernation_Cycle_01(automation_xiaowei_connect):
    cycle_time = 4  #duration, unit - h
    dut = automation_xiaowei_connect[0]
    current_name = dut.bluetooth.get_name()
    phone = automation_xiaowei_connect[1]
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weekday"]))
    response_text = query_response_dict["query_weekday"][query_text]
    assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query the query_weather", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"

    test_step(1, "Set dut auto off", dut)
    assert dut.device.enable_auto_off() == '5', "Fail to set auto off timer as 5"
    base_t = time.time()
    current_t = time.time()
    while float(current_t-base_t) <= float(cycle_time*3600):
        test_step(2, "Check if dut power off in 10 minutes", dut)
        for i in [300, 60, 60, 60, 60, 60, 60]:
            wait(i)
            if dut.status.get_sink_state() == SinkStates.STANDBY:
                break
        else:
            assert False, "Dut didn't power off in 10 minutes"
        test_step(3, "Power on dut", dut)
        assert dut.key.press_power_on(), "Fail to power on dut"
        wait(3)
        test_step(4, "Dut connect to phone and xiaowei", dut)
        assert phone.launch_application(PhoneAppType.BLUETOOTH), "Failed to switch to bluetooth settings"
        if not phone.bluetooth.bt_is_connected_to(current_name):
            assert phone.bluetooth.connect_paired_device(current_name), "Failed to dut via bluetooth"
        assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to switch to Xiaowei"
        test_xiaowei_query(5, 6)
        current_t = time.time()
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_VPA_Button_Stress_01(automation_xiaowei_connect):
    dut = automation_xiaowei_connect[0]
    phone = automation_xiaowei_connect[1]
    assert phone.xiaowei.verify_device_icon(), "Xiaowei connection fail"
    cycle = 40
    for i in range(cycle):
        press_time = random.choice([0.35, 1, 2, 3, 5, 8, 13, 21])
        logger.info("VPA button stress for %d times, %d" % (cycle, i + 1))
        test_step(1, "Power VPA button for %d second" % press_time, dut)
        dut.key.press_and_release(keys=Buttons.VPA, press_duration_sec=press_time)
        wait(2)

    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weekday"]))
    response_text = query_response_dict["query_weekday"][query_text]
    test_step(2, "Test xiaowei voice query the query_weather", dut)
    XiaoweiSupport.test_vpa(dut, query_text)
    assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
    test_step(3, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
    assert phone.xiaowei.verify_query_response_text(query_text, response_text), "xiaowei query or response failed"
    phone.xiaowei.swip_down(n=8)