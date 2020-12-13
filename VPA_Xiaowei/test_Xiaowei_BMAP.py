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
def test_Retrieve_PTT_Configuration_Before_Setting_Up_VPA_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    current_name = dut.bluetooth.get_name()
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]
    def test_xiaowei_query(stepnum1, stepnum2):
        test_step(stepnum1, "Test xiaowei voice query the weather of a city", dut)
        XiaoweiSupport.test_vpa(dut, query_text)
        assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
        test_step(stepnum2, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
        assert phone.xiaowei.verify_query_response_text(query_text, response_text,
                                                        response_with_icon=True), "xiaowei query or response failed"
    test_step(1, "Perform factory default", dut)
    assert dut.device.perform_factory_default(restore_name=True, wait_time_after_fd=5), "Failed to perform factory default"
    dut.manager.initialize()
    test_step(2, "Check PPT of native VPA", dut)
    assert dut.status.get_push_to_talk_vpa_status() == '2', "Failed to check PTT status of native VPA"

    phone.launch_application(PhoneAppType.BLUETOOTH)
    for device in phone.bluetooth.bt_get_pairlist():
        phone.bluetooth.bt_unpair(device)
    # don't use Precondition.set_discoverable(dut), because Precondition.set_discoverable(dut) may power cycle dut.
    # For earbuds test, initialize() is needed after power cycle
    # dut.bluetooth.set_discoverable() just send a BMAP to dut
    dut.bluetooth.set_discoverable()
    phone.bluetooth.bt_radio(enable='off')
    phone.bluetooth.bt_radio(enable='on')
    assert phone.bluetooth.bt_connect(current_name), "Failed to reconnect dut via bluetooth"
    test_step(3, "Switch to xiaowei APP", dut)
    assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to switch to Xiaowei"
    test_step(4, "Verify if xiaowei connect to dut", dut)
    assert phone.xiaowei.insure_device_connection(), "Failed to connect dut via xiaowei"
    test_step(5, "Verify if xiaowei connect to dut", dut)
    #because product change VPA slowly
    for _ in range(5):
        wait(1)
        if dut.status.get_push_to_talk_vpa_status() == '3':
            break
    else:
        assert False, "Failed to check PTT status of xiaowei VPA"
    test_xiaowei_query(6, 7)
    phone.xiaowei.swip_down(n=8)

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Set_PTT_For_All_VPA_Before_Setting_Up_VPA_01(automation_xiaowei_ux):
    dut = automation_xiaowei_ux[0]
    phone = automation_xiaowei_ux[1]
    current_name = dut.bluetooth.get_name()
    query_response_dict = XiaoweiSupport.xw_query_response_dict()
    query_text = random.choice(list(query_response_dict["query_weather"]))
    response_text = query_response_dict["query_weather"][query_text]
    test_step(1, "Perform factory default", dut)
    assert dut.device.perform_factory_default(restore_name=True, wait_time_after_fd=5), "Failed to perform factory default"
    dut.manager.initialize()
    test_step(2, "Check PPT of native VPA", dut)
    assert dut.status.get_push_to_talk_vpa_status() == '2', "Failed to check PTT status of native VPA"
    test_step(3, "Set and check PPT of google VPA", dut)
    dut.device.set_google_assistant_as_push_to_talk_vpa()
    assert dut.status.get_push_to_talk_vpa_status() == '0', "Failed to check PTT status of Google VPA"
    dut.device.set_alexa_as_push_to_talk_vpa()
    test_step(4, "Set and check PPT of alexa VPA", dut)
    assert dut.status.get_push_to_talk_vpa_status() == '1', "Failed to check PTT status of Alexa VPA"
    test_step(5, "Set and check PPT of xiaowei VPA", dut)
    dut.device.set_xiaowei_as_push_to_talk_vpa()
    assert dut.status.get_push_to_talk_vpa_status() == '3', "Failed to check PTT status of Xiaowei VPA"

    phone.launch_application(PhoneAppType.BLUETOOTH)
    for device in phone.bluetooth.bt_get_pairlist():
        phone.bluetooth.bt_unpair(device)
    # don't use Precondition.set_discoverable(dut), because Precondition.set_discoverable(dut) may power cycle dut.
    # For earbuds test, initialize() is needed after power cycle
    # dut.bluetooth.set_discoverable() just send a BMAP to dut
    dut.bluetooth.set_discoverable()
    phone.bluetooth.bt_radio(enable='off')
    phone.bluetooth.bt_radio(enable='on')
    assert phone.bluetooth.bt_connect(current_name), "Failed to reconnect dut via bluetooth"
    test_step(6, "Switch to xiaowei APP", dut)
    assert phone.launch_application(PhoneAppType.XIAOWEI), "Failed to switch to Xiaowei"
    test_step(7, "Verify if xiaowei connect to dut", dut)
    assert phone.xiaowei.insure_device_connection(), "Failed to connect dut via xiaowei"
    test_step(8, "Test xiaowei voice query the weather of a city", dut)
    XiaoweiSupport.test_vpa(dut, query_text)
    assert XiaoweiSupport.test_xiaowei_vpa(), "xiaowei recording or streaming failed"
    test_step(9, "Verify that the text of this query and response in xiaowei APP is correct or not", dut)
    assert phone.xiaowei.verify_query_response_text(query_text, response_text, response_with_icon=True), "xiaowei query or response failed"
    phone.xiaowei.swip_down(n=8)

