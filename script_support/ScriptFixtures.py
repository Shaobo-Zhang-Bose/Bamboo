#!/usr/bin/python
# -*- coding  utf-8 -*-
#
#  Organization   BOSE CORPORATION
#  Copyright      COPYRIGHT 2018 BOSE CORPORATION ALL RIGHTS RESERVED.
#                 This program may not be reproduced, in whole or in part in any
#                 form or any means whatsoever without the written permission of
#                     BOSE CORPORATION
#                     The Mountain,
#                     Framingham, MA 01701-9168
################################################################################
"""
Fixtures to use in test cases and test suite routines
"""

import pytest
from wham_automation.script_support.CommonFixture import PhoneAppType, automation_context


@pytest.fixture(scope='function')
def dut_precondition_connected_activated_in_xiaowei(automation_context):
    """
    Xiaowei test case setup
    :param automation_context:
    :return:
    """
    dut = automation_context.dut_list[0]
    current_name = dut.bluetooth.get_name()
    phone = automation_context.phones[0]
    dut.manager.initialize()
    phone.launch_application(PhoneAppType.BLUETOOTH)
    if_connect_dut = phone.bluetooth.bt_is_connected_to(current_name)
    if not if_connect_dut:
        # don't use Precondition.set_discoverable(dut), because Precondition.set_discoverable(dut) may power cycle dut.
        # For earbuds test, initialize() is needed after power cycle
        # dut.bluetooth.set_discoverable() just send a BMAP to dut
        dut.bluetooth.set_discoverable()
        phone.bluetooth.bt_radio(enable='off')
        phone.bluetooth.bt_radio(enable='on')
        if_connect_dut = phone.bluetooth.bt_connect(current_name)
    phone.bluetooth.kill_bluetooth_app()
    phone._set_current_app_to_none()
    if not if_connect_dut:
        return if_connect_dut
    else:
        return automation_context