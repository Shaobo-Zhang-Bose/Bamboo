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
A module for handling the dut.Manager interface to test cases. This is layer fit to different products
"""
import time
from wham_automation.lib.framework.dut_interfaces.DutInterfaceBase import DutInterfaceBase
from wham_automation.lib.framework.Configs.CommandType import CommandType
from wham_automation.config_types import EarbudMode
from wham_automation.lib.framework.Configs.FrameworkConstants import EarbudEvent
from wham_automation.lib.framework.Configs.ProductInfo import Buttons

class Manager(DutInterfaceBase):

    def __init__(self, dut, connection):
        super().__init__(dut, connection)

    def initialize(self):
        if ('REVEL' in self._dut.product_info.name.upper()) or ('LANDO' in self._dut.product_info.name.upper()):
            self._dut.device.enable_operational_charging()
            self._dut.device.simulate_earbud_event(EarbudEvent.CHARGER_ATTACHED)
            self._dut.device.simulate_earbud_event(EarbudEvent.CHARGER_DETACHED)
            self._dut.device.simulate_earbud_event(EarbudEvent.START_OF_DON)
            self._dut.device.simulate_earbud_event(EarbudEvent.IN_EAR_DETECTED)
        else:
            self._dut.device.enable_operational_charging()

    def vpa_tap_hold(self, hold_seconds, how_many_times=1):
        if ('REVEL' in self._dut.product_info.name.upper()) or ('LANDO' in self._dut.product_info.name.upper()):
            self._dut.captouch.captouch_tap_and_hold()
            time.sleep(hold_seconds)
            self._dut.captouch.captouch_tap_and_hold_release()
        elif 'GOODYEAR' in self._dut.product_info.name.upper():
            self._dut.key.press_and_release(Buttons.VPA, press_duration_sec=hold_seconds,
                                           how_many_times=how_many_times)
        else:
            pass

    def multi_connection_supprot(self):
        if ('REVEL' in self._dut.product_info.name.upper()) or ('LANDO' in self._dut.product_info.name.upper()):
            return False
        else:
            return True

    def cnc_tap_hold(self, hold_seconds=0.35, how_many_times=1):
        if ('REVEL' in self._dut.product_info.name.upper()) or ('LANDO' in self._dut.product_info.name.upper()):
            self._dut.captouch.captouch_tap_and_hold()
            time.sleep(hold_seconds)
            self._dut.captouch.captouch_tap_and_hold_release()
        elif 'GOODYEAR' in self._dut.product_info.name.upper():
            self._dut.key.press_and_release(Buttons.ANR_CNC, press_duration_sec=hold_seconds,
                                            how_many_times=how_many_times)
        else:
            pass
