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
Test Case ID : Xiaowei_NC
Description  : Xiaowei NC for adjust NC level
Pre-condition: Xiaowei NC-Standby
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
from wham_automation.test_scripts.Bamboo.VPA_Xiaowei.Xiaowei_Support import XiaoweiSupport
import wham_automation.test_scripts.Bamboo.VPA_Xiaowei.Xiaowei_NC_EQ_Support as Xiaowei_NC_EQ_Support

@pytest.fixture(scope='function')
def automation_xiaowei_nc_eq(dut_precondition_connected_activated_in_xiaowei):
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
def test_Xiaowei_NC_Support_01(automation_xiaowei_nc_eq):
    dut = automation_xiaowei_nc_eq[0]
    phone = automation_xiaowei_nc_eq[1]

    test_results = list()
    test_results.append("*" * 150)
    test_results.append("Test logs".center(150, "*"))
    test_results.append("*" * 150)
    test_results.append("%-30s%-30s%-30s%-30s%-30s" % ("query_nc_text", "query_text_in_xw", "source_nc_level/state", "current_nc_level/state", "test_result"))

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def handle_xiaowei_nc(xiaowei_nc_support, test_results):
        assert xiaowei_nc_support.perform_nc_query(), "xiaowei recording or streaming failed"
        test_result = xiaowei_nc_support.check_result()
        test_results.append(test_result)
        assert phone.xiaowei.close_app(), "Failed to close xiaowei"
        assert phone.xiaowei.launch_app(), "Failed to re-open xiaowei"

    test_step(1, "Test xiaowei to get current nc level", dut)
    test_results.append("Get current NC level".center(150, "*"))
    current_nc_level = Xiaowei_NC_EQ_Support.current_nc_level
    for query_text in current_nc_level:
        source_nc_level = random.randint(0, 10)
        target_nc_level = source_nc_level
        xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_level, target_nc_level, query_text, "nc_level")
        xiaowei_nc_support.adjust_nc_level()
        handle_xiaowei_nc(xiaowei_nc_support, test_results)

    test_step(2, "Test xiaowei to increase nc level", dut)
    test_results.append("Increase NC level".center(150, "*"))
    increase_nc_level = Xiaowei_NC_EQ_Support.increase_nc_level
    for query_text in increase_nc_level:
        source_nc_level = random.randint(0, 9)
        target_nc_level = source_nc_level + 1
        xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_level, target_nc_level, query_text, "nc_level")
        xiaowei_nc_support.adjust_nc_level()
        handle_xiaowei_nc(xiaowei_nc_support, test_results)

    test_step(3, "Test xiaowei to decrease nc level", dut)
    test_results.append("Decrease NC level".center(150, "*"))
    decrease_nc_level = Xiaowei_NC_EQ_Support.decrease_nc_level
    for query_text in decrease_nc_level:
        source_nc_level = random.randint(1, 10)
        target_nc_level = source_nc_level - 1
        xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_level, target_nc_level, query_text, "nc_level")
        xiaowei_nc_support.adjust_nc_level()
        handle_xiaowei_nc(xiaowei_nc_support, test_results)

    test_step(4, "Test xiaowei to set nc to specific level", dut)
    test_results.append("Set NC to specific level".center(150, "*"))
    set_nc_to_specific_level = Xiaowei_NC_EQ_Support.set_nc_to_specific_level
    all_levels_list = [i for i in range(0, 11)]
    for query_text in set_nc_to_specific_level:
        source_nc_level = random.choice(all_levels_list)
        target_nc_level = random.choice(list(set(all_levels_list).difference({source_nc_level})))
        query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_nc_level])
        xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_level, target_nc_level, query_text, "nc_level")
        xiaowei_nc_support.adjust_nc_level()
        handle_xiaowei_nc(xiaowei_nc_support, test_results)

    test_step(5, "Test xiaowei to set nc level to max", dut)
    test_results.append("Set NC level to max".center(150, "*"))
    set_nc_level_to_max = Xiaowei_NC_EQ_Support.set_nc_level_to_max
    for query_text in set_nc_level_to_max:
        source_nc_level = random.randint(0, 9)
        target_nc_level = 10
        xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_level, target_nc_level, query_text, "nc_level")
        xiaowei_nc_support.adjust_nc_level()
        handle_xiaowei_nc(xiaowei_nc_support, test_results)

    test_step(6, "Test xiaowei to set nc level to min", dut)
    test_results.append("Set NC level to min".center(150, "*"))
    set_nc_level_to_min = Xiaowei_NC_EQ_Support.set_nc_level_to_min
    for query_text in set_nc_level_to_min:
        source_nc_level = random.randint(1, 10)
        target_nc_level = 0
        xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_level, target_nc_level, query_text, "nc_level")
        xiaowei_nc_support.adjust_nc_level()
        handle_xiaowei_nc(xiaowei_nc_support, test_results)

    test_step(7, "Test xiaowei to turn nc on", dut)
    test_results.append("Turn NC on".center(150, "*"))
    set_nc_on = Xiaowei_NC_EQ_Support.turn_nc_on
    for query_text in set_nc_on:
        source_nc_state = 0
        target_nc_state = 1
        xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_state, target_nc_state, query_text, "nc_state")
        xiaowei_nc_support.turn_nc_off()
        handle_xiaowei_nc(xiaowei_nc_support, test_results)

    test_step(8, "Test xiaowei to turn nc off", dut)
    test_results.append("Turn NC off".center(150, "*"))
    set_nc_off = Xiaowei_NC_EQ_Support.turn_nc_off
    for query_text in set_nc_off:
        source_nc_state = 1
        target_nc_state = 0
        xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_state, target_nc_state, query_text, "nc_state")
        xiaowei_nc_support.turn_nc_on()
        handle_xiaowei_nc(xiaowei_nc_support, test_results)

    for test_result in test_results:
        if isinstance(test_result, str):
            print(test_result)

        if isinstance(test_result, list):
            for each_item in test_result:
                print(str(each_item).ljust(30 - len(str(each_item))), end="")
            print()

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Set_All_NC_Levels_01(automation_xiaowei_nc_eq):
    dut = automation_xiaowei_nc_eq[0]
    phone = automation_xiaowei_nc_eq[1]
    test_results = list()
    test_results.append("*" * 150)
    test_results.append("Test logs".center(150, "*"))
    test_results.append("*" * 150)
    test_results.append("%-30s%-30s%-30s%-30s%-30s" % ("query_nc_text", "query_text_in_xw", "source_nc_level/state", "current_nc_level/state", "test_result"))

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def handle_xiaowei_nc(xiaowei_nc_support, test_results):
        assert xiaowei_nc_support.perform_nc_query(), "xiaowei recording or streaming failed"
        test_result = xiaowei_nc_support.check_result()
        test_results.append(test_result)
        assert phone.xiaowei.close_app(), "Failed to close xiaowei"
        assert phone.xiaowei.launch_app(), "Failed to re-open xiaowei"

    test_step(1, "Test xiaowei to set all nc levels", dut)
    test_results.append("Set all nc levels".center(150, "-"))
    set_nc_to_specific_level = Xiaowei_NC_EQ_Support.set_nc_to_specific_level
    all_levels_list = [i for i in range(0, 11)]
    for query_text in set_nc_to_specific_level:
        for level in all_levels_list:
            target_nc_level = level
            source_nc_level = random.choice(list(set(all_levels_list).difference({level})))
            real_query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_nc_level])
            xiaowei_nc_support = Xiaowei_NC_EQ_Support.Xiaowei_NC_Support(dut, phone, source_nc_level, target_nc_level, real_query_text, "nc_level")
            xiaowei_nc_support.adjust_nc_level()
            handle_xiaowei_nc(xiaowei_nc_support, test_results)

    for test_result in test_results:
        if isinstance(test_result, str):
            print(test_result)
        if isinstance(test_result, list):
            for each_item in test_result:
                print(str(each_item).ljust(30 - len(str(each_item))), end="")
            print()
            
@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_EQ_Support_01(automation_xiaowei_nc_eq):
    dut = automation_xiaowei_nc_eq[0]
    phone = automation_xiaowei_nc_eq[1]

    test_results = list()
    test_results.append("*" * 150)
    test_results.append("Test logs".center(150, "*"))
    test_results.append("*" * 150)
    test_results.append("%-30s%-30s%-30s%-30s%-30s" % ("query_eq_text", "query_text_in_xw", "source_eq_level", "current_eq_level", "test_result"))

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def handle_xiaowei_eq(xiaowei_eq, test_results):
        assert xiaowei_eq.perform_eq_query(), "xiaowei recording or streaming failed"
        test_result = xiaowei_eq.check_result()
        test_results.append(test_result)
        assert phone.xiaowei.close_app(), "Failed to close xiaowei"
        assert phone.xiaowei.launch_app(), "Failed to re-open Xiaowei"

    test_step(1, "Test xiaowei to increase treble level", dut)
    test_results.append("Increase treble level".center(150, "-"))
    increase_treble_level = Xiaowei_NC_EQ_Support.increase_treble_level
    for query_text in increase_treble_level:
        source_eq_level = random.randint(-10, 9)
        target_eq_level = source_eq_level + 1
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "treble")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(2, "Test xiaowei to increase mid level", dut)
    test_results.append("Increase mid level".center(150, "-"))
    increase_mid_level = Xiaowei_NC_EQ_Support.increase_mid_level
    for query_text in increase_mid_level:
        source_eq_level = random.randint(-10, 9)
        target_eq_level = source_eq_level + 1
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "mid")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(3, "Test xiaowei to increase bass level", dut)
    test_results.append("Increase bass level".center(150, "-"))
    increase_bass_level = Xiaowei_NC_EQ_Support.increase_bass_level
    for query_text in increase_bass_level:
        source_eq_level = random.randint(-10, 9)
        target_eq_level = source_eq_level + 1
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "bass")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(4, "Test xiaowei to decrease treble level", dut)
    test_results.append("Decrease treble level".center(150, "-"))
    decrease_treble_level = Xiaowei_NC_EQ_Support.decrease_treble_level
    for query_text in decrease_treble_level:
        source_eq_level = random.randint(-9, 10)
        target_eq_level = source_eq_level - 1
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "treble")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(5, "Test xiaowei to decrease mid level", dut)
    test_results.append("Decrease mid level".center(150, "-"))
    decrease_mid_level = Xiaowei_NC_EQ_Support.decrease_mid_level
    for query_text in decrease_mid_level:
        source_eq_level = random.randint(-9, 10)
        target_eq_level = source_eq_level - 1
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "mid")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(6, "Test xiaowei to decrease bass level", dut)
    test_results.append("Decrease bass level".center(150, "-"))
    decrease_bass_level = Xiaowei_NC_EQ_Support.decrease_bass_level
    for query_text in decrease_bass_level:
        source_eq_level = random.randint(-9, 10)
        target_eq_level = source_eq_level - 1
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "bass")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(7, "Test xiaowei to set treble level to max", dut)
    test_results.append("Set treble level to max".center(150, "-"))
    set_treble_level_to_max = Xiaowei_NC_EQ_Support.set_treble_level_to_max
    for query_text in set_treble_level_to_max:
        source_eq_level = random.randint(-10, 9)
        target_eq_level = 10
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "treble")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(8, "Test xiaowei to set mid level to max", dut)
    test_results.append("Set mid level to max".center(150, "-"))
    set_mid_level_to_max = Xiaowei_NC_EQ_Support.set_mid_level_to_max
    for query_text in set_mid_level_to_max:
        source_eq_level = random.randint(-10, 9)
        target_eq_level = 10
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "mid")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(9, "Test xiaowei to set bass level to max", dut)
    test_results.append("Set bass level to max".center(150, "-"))
    set_bass_level_to_max = Xiaowei_NC_EQ_Support.set_bass_level_to_max
    for query_text in set_bass_level_to_max:
        source_eq_level = random.randint(-10, 9)
        target_eq_level = 10
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "bass")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(10, "Test xiaowei to set treble level to min", dut)
    test_results.append("Set treble level to min".center(150, "-"))
    set_treble_level_to_min = Xiaowei_NC_EQ_Support.set_treble_level_to_min
    for query_text in set_treble_level_to_min:
        source_eq_level = random.randint(-9, 10)
        target_eq_level = -10
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "treble")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(11, "Test xiaowei to set mid level to min", dut)
    test_results.append("Set mid level to min".center(150, "-"))
    set_mid_level_to_min = Xiaowei_NC_EQ_Support.set_mid_level_to_min
    for query_text in set_mid_level_to_min:
        source_eq_level = random.randint(-9, 10)
        target_eq_level = -10
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "mid")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(12, "Test xiaowei to set bass level to min", dut)
    test_results.append("Set bass level to min".center(150, "-"))
    set_bass_level_to_min = Xiaowei_NC_EQ_Support.set_bass_level_to_min
    for query_text in set_bass_level_to_min:
        source_eq_level = random.randint(-9, 10)
        target_eq_level = -10
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "bass")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(13, "Test xiaowei to set treble level to default", dut)
    test_results.append("Set treble level to default".center(150, "-"))
    set_treble_level_to_default = Xiaowei_NC_EQ_Support.set_treble_level_to_default
    for query_text in set_treble_level_to_default:
        source_eq_level = random.randint(-10, 10)
        target_eq_level = 0
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "treble")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(14, "Test xiaowei to set mid level to default", dut)
    test_results.append("Set mid level to default".center(150, "-"))
    set_mid_level_to_default = Xiaowei_NC_EQ_Support.set_mid_level_to_default
    for query_text in set_mid_level_to_default:
        source_eq_level = random.randint(-10, 10)
        target_eq_level = 0
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "mid")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(15, "Test xiaowei to set bass level to default", dut)
    test_results.append("Set bass level to default".center(150, "-"))
    set_bass_level_to_default = Xiaowei_NC_EQ_Support.set_bass_level_to_default
    for query_text in set_bass_level_to_default:
        source_eq_level = random.randint(-10, 10)
        target_eq_level = 0
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "bass")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(16, "Test xiaowei to set treble to specific level", dut)
    test_results.append("Set treble to specific level".center(150, "-"))
    set_treble_to_specific_level = Xiaowei_NC_EQ_Support.set_treble_to_specific_level
    all_levels_list = [i for i in range(-10, 11)]
    for query_text in set_treble_to_specific_level:
        source_eq_level = random.choice(all_levels_list)
        target_eq_level = random.choice(list(set(all_levels_list).difference({source_eq_level})))
        query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_eq_level])
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "treble")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(17, "Test xiaowei to set mid to specific level", dut)
    test_results.append("Set mid to specific level".center(150, "-"))
    set_mid_to_specific_level = Xiaowei_NC_EQ_Support.set_mid_to_specific_level
    all_levels_list = [i for i in range(-10, 11)]
    for query_text in set_mid_to_specific_level:
        source_eq_level = random.choice(all_levels_list)
        target_eq_level = random.choice(list(set(all_levels_list).difference({source_eq_level})))
        query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_eq_level])
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "mid")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(18, "Test xiaowei to set bass to specific level", dut)
    test_results.append("Set bass to specific level".center(150, "-"))
    set_bass_to_specific_level = Xiaowei_NC_EQ_Support.set_bass_to_specific_level
    all_levels_list = [i for i in range(-10, 11)]
    for query_text in set_bass_to_specific_level:
        source_eq_level = random.choice(all_levels_list)
        target_eq_level = random.choice(list(set(all_levels_list).difference({source_eq_level})))
        query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_eq_level])
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, "bass")
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(19, "Test xiaowei to set multiple eqs to specific level", dut)
    test_results.append("Set multiple eqs to specific level".center(150, "-"))
    set_multiple_eqs_to_specific_level = Xiaowei_NC_EQ_Support.set_multiple_eqs_to_specific_level
    all_levels_list = [i for i in range(-10, 11)]
    for query_list in set_multiple_eqs_to_specific_level:
        source_eq_level = random.choice(all_levels_list)
        target_eq_level = random.choice(list(set(all_levels_list).difference({source_eq_level})))
        query_text = query_list[0]
        query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_eq_level])
        xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, query_text, *query_list[1])
        xiaowei_eq_support.adjust_eq_level()
        handle_xiaowei_eq(xiaowei_eq_support, test_results)

    for test_result in test_results:
        if isinstance(test_result, str):
            print(test_result)

        if isinstance(test_result, list):
            for each_item in test_result:
                print(str(each_item).ljust(30 - len(str(each_item))), end="")
            print()

@ScriptCommon()
@TestFilters(scope=1, phones=[[PhoneType.ANY]])
def test_Xiaowei_Set_All_EQ_Levels_01(automation_xiaowei_nc_eq):
    dut = automation_xiaowei_nc_eq[0]
    phone = automation_xiaowei_nc_eq[1]
    test_results = list()
    test_results.append("*" * 150)
    test_results.append("Test logs".center(150, "*"))
    test_results.append("*" * 150)
    test_results.append("%-30s%-30s%-30s%-30s%-30s" % ("query_eq_text", "query_text_in_xw", "source_eq_level", "current_eq_level", "test_result"))

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def handle_xiaowei_eq(xiaowei_eq, test_results):
        assert xiaowei_eq.perform_eq_query(), "xiaowei recording or streaming failed"
        test_result = xiaowei_eq.check_result()
        test_results.append(test_result)
        assert phone.xiaowei.close_app(), "Failed to close xiaowei"
        assert phone.xiaowei.launch_app(), "Failed to re-open Xiaowei"

    test_step(1, "Test xiaowei to set all treble levels", dut)
    test_results.append("Set all treble levels".center(150, "-"))
    set_treble_to_specific_level = Xiaowei_NC_EQ_Support.set_treble_to_specific_level
    all_levels_list = [i for i in range(-10, 11)]
    for query_text in set_treble_to_specific_level:
        for level in all_levels_list:
            target_eq_level = level
            source_eq_level = random.choice(list(set(all_levels_list).difference({level})))
            real_query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_eq_level])
            xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, real_query_text, "treble")
            xiaowei_eq_support.adjust_eq_level()
            handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(2, "Test xiaowei to set all mid levels", dut)
    test_results.append("Set all mid levels".center(150, "-"))
    set_mid_to_specific_level = Xiaowei_NC_EQ_Support.set_mid_to_specific_level
    all_levels_list = [i for i in range(-10, 11)]
    for query_text in set_mid_to_specific_level:
        for level in all_levels_list:
            target_eq_level = level
            source_eq_level = random.choice(list(set(all_levels_list).difference({level})))
            real_query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_eq_level])
            xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, real_query_text, "mid")
            xiaowei_eq_support.adjust_eq_level()
            handle_xiaowei_eq(xiaowei_eq_support, test_results)

    test_step(3, "Test xiaowei to set all bass levels", dut)
    test_results.append("Set all bass levels".center(150, "-"))
    set_bass_to_specific_level = Xiaowei_NC_EQ_Support.set_bass_to_specific_level
    all_levels_list = [i for i in range(-10, 11)]
    for query_text in set_bass_to_specific_level:
        for level in all_levels_list:
            target_eq_level = level
            source_eq_level = random.choice(list(set(all_levels_list).difference({level})))
            real_query_text = query_text.replace("#", Xiaowei_NC_EQ_Support.Matching_Table_of_Numbers_and_Chinese_Characters[target_eq_level])
            xiaowei_eq_support = Xiaowei_NC_EQ_Support.Xiaowei_EQ_Support(dut, phone, source_eq_level, target_eq_level, real_query_text, "bass")
            xiaowei_eq_support.adjust_eq_level()
            handle_xiaowei_eq(xiaowei_eq_support, test_results)

    for test_result in test_results:
        if isinstance(test_result, str):
            print(test_result)
        if isinstance(test_result, list):
            for each_item in test_result:
                print(str(each_item).ljust(30 - len(str(each_item))), end="")
            print()



