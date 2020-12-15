# -*- coding  utf-8 -*-
#
#  Organization  BOSE CORPORATION
#  Copyright     COPYRIGHT 2018 BOSE CORPORATION ALL RIGHTS RESERVED.
#                This program may not be reproduced, in whole or in part in any
#                form or any means whatsoever without the written permission of
#                    BOSE CORPORATION
#                    The Mountain,
#                    Framingham, MA 01701-9168
#
###############################################################################
"""
A test suite for running all Connection test cases together.

The aim is to try to get these tests to run faster by doing them all through
one module.

For the time being, if this file is imported, it will reorder the test
functions it contains. This will only affect execution if running multiple
sub-feature files together after having imported this (which is a weird case...
you'd run the tests multiple times?).

"""
#pylint: disable=unused-import

# Import all the fixtures used.
from wham_automation.script_support.CommonFixture import automation_context, setup_module_test_environment, setup_test_environment
from wham_automation.script_support.SoftAssert import soft_assert_fixture
from wham_automation.script_support.ScriptFixtures import dut_precondition_poweroff, dut_precondition_poweroff_factory_reset, dut_precondition_discoverable, dut_precondition_poweron_connected, dut_precondition_connected, dut_precondition_connected_poweroff, dut_precondition_poweron, dut_precondition_connected_exactly_once
from wham_automation.test_scripts.DUT_Connection.Connection_Smoke.Connection_Smoke_Fixtures import enable_auto_off_fixture
from wham_automation.script_support.ScriptFixtures import dut_precondition_poweron_connected_disconnected, dut_precondition_poweron_connected_disconnected_ANR

from wham_automation.script_support.Reorder import reorder_tests, FeatureStartingOrder

# Then import all the test functions
from wham_automation.test_scripts.VPA.VPA_Xiaowei.test_Xiaowei_Connect import *
from wham_automation.test_scripts.VPA.VPA_Xiaowei.test_Xiaowei_UX import *
from wham_automation.test_scripts.VPA.VPA_Xiaowei.test_Xiaowei_BMAP import *
from wham_automation.test_scripts.VPA.VPA_Xiaowei.test_Xiaowei_NC_EQ import *

reorder_tests(
    FeatureStartingOrder.VPA_XIAOWEI,
    1,  # One Android phone.
    1,  # one iPhone.
    (
        test_Xiaowei_Accept_Prompt_01,
        test_Xiaowei_Reopen_Cycle_01,
        test_Xiaowei_Disconnect_Cycle_01,
        test_Xiaowei_Dut_Power_Cycle_01,
        test_Xiaowei_Bluetooth_Disable_Cycle_01,
        test_Xiaowei_Hibernation_Cycle_01,
        test_Xiaowei_VPA_Button_Stress_01,
        test_Retrieve_PTT_Configuration_Before_Setting_Up_VPA_01,
        test_Set_PTT_For_All_VPA_Before_Setting_Up_VPA_01,
        test_Xiaowei_NC_Support_01,
        test_Xiaowei_EQ_Support_01,
        test_Xiaowei_Show_Different_Device_Name_01,
        test_Xiaowei_Voice_Query_Weekday_01,
        test_Xiaowei_Voice_Query_Weather_01,
        test_Xiaowei_Voice_Query_Weather_Cycle_01,
        test_Xiaowei_Ping_Pong_Voice_Query_Cycle_01,
        test_Xiaowei_Interrupt_Response_By_New_Voice_Query_Cycle_01,
        test_Xiaowei_Disconnect_Connect_HP_and_Query_Cycle_01,
        test_Xiaowei_Voice_Query_For_an_Hour_01,
        test_Xiaowei_Response_Conversation_01,
        test_Xiaowei_Response_CNC_01,
        test_Xiaowei_Native_Switch_Cycle_01,
        test_Xiaowei_Cancel_Prompt_Request_01,
        test_Xiaowei_Control_Story_Music_Playing_Through_VPA_Query_01,
        test_Xiaowei_Control_Story_Music_Playing_Through_Cap_Touch_01,
        test_Xiaowei_Control_VPA_Response_Volume_Through_Captouch_Cycle_01,
        test_Xiaowei_Reconection_After_Clearing_PDL_01,
        test_VPA_Status_After_Factory_Default_01,
        test_Xiaowei_Query_Response_With_Unsupported_Captouch_Gestures,
        test_Xiaowei_While_HP_Is_In_Discoverable_State_01
    ),
)
