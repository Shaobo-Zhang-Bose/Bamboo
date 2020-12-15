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
import re
import random

from wham_automation.lib.framework.Configs.FrameworkConstants import PhoneType
from wham_automation.lib.mobile.scenario.PhoneObject import PhoneAppType
from wham_automation.script_support.AssertHelpers import SinkStates
from wham_automation.lib.framework.Configs.ProductInfo import Buttons
from wham_automation.script_support.ScriptHelper import wait
from wham_automation.utils.log import logger
from wham_automation.lib.mobile.constants.MobileConstants import const
from wham_automation.test_scripts.Bamboo.VPA_Xiaowei.Xiaowei_Support import XiaoweiSupport

Matching_Table_of_Numbers_and_Chinese_Characters = {
    -1: "负一", -2: "负二", -3: "负三", -4: "负四", -5: "负五", -6: "负六", -7: "负七", -8: "负八",  -9: "负九", -10: "负十",
    0: "零", 1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八",  9: "九", 10: "十"
}

Matching_Table_of_Correct_Words_and_Wrong_Words = {
    "中音": ["中英", "终因", "中医", "声音", "重音"],
    "级": ["集"]
}

################################################## Query Base for NC ###################################################

current_nc_level = [
    "降噪等级", "降噪等级是多少", "当前降噪等级", "当前降噪等级是多少", "现在降噪等级", "现在降噪等级是多少",
    "消噪等级", "消噪等级是多少", "当前消噪等级", "当前消噪等级是多少", "现在消噪等级", "现在消噪等级是多少"
 ]

increase_nc_level = [
    "降噪加", "降噪增加", "降噪增强", "增加降噪", "增强降噪", "调高降噪", "提高降噪",
    "消噪加", "消噪增加", "消噪增强", "增加消噪", "增强消噪", "调高消噪", "提高消噪",
    "周围太吵了", "噪音太多了"
]

decrease_nc_level = [
    "降噪减", "降噪减少", "降噪减弱", "降低降噪", "减少降噪", "调低降噪", "减弱降噪",
    "消噪减", "消噪减少", "消噪减弱", "降低消噪", "减少消噪", "调低消噪", "减弱消噪"
]

set_nc_to_specific_level = [
    "降噪#", "降噪至#", "降噪调至#", "降噪调到#", "降噪等级#", "#级降噪", "设为#级降噪", "把降噪调至#", "把降噪调到#",
    "消噪#", "消噪至#", "消噪调至#", "消噪调到#", "消噪等级#", "#级消噪", "设为#级消噪", "把消噪调至#", "把消噪调到#",
]

set_nc_level_to_max = [
    "降噪最高", "降噪最大", "降噪调到最高", "降噪调到最大",
    "降噪调至最高", "降噪调至最大", "降噪升到最高", "降噪升到最大",
    "消噪最高", "消噪最大", "消噪调到最高", "消噪调到最大",
    "消噪调至最高", "消噪调至最大", "消噪升到最高", "消噪升到最大"
]

set_nc_level_to_min = [
    "降噪最低", "降噪最小", "降噪调到最低", "降噪调到最小",
    "降噪调至最低", "降噪调至最小", "降噪升到最低", "降噪升到最小",
    "消噪最低", "消噪最小", "消噪调到最低", "消噪调到最小",
    "消噪调至最低", "消噪调至最小", "消噪升到最低", "消噪升到最小"
]

turn_nc_on = [
    "打开降噪", "开启降噪", "降噪开", "降噪打开", "降噪开启",
    "打开消噪", "开启消噪", "消噪开", "消噪打开", "消噪开启"
]

turn_nc_off = [
    "关闭降噪", "取消降噪", "降噪关", "降噪关闭", "降噪取消",
    "关闭消噪", "取消消噪", "消噪关", "消噪关闭", "消噪取消"
]

turn_conversation_mode_on = [
    "打开对话模式", "开启对话模式", "对话模式开", "对话模式打开", "对话模式开启",
]

turn_conversation_mode_off = [
    "关闭对话模式", "取消对话模式", "对话模式关", "对话模式关闭", "对话模式取消",
]

turn_transparency_mode_on = [
    "打开通透模式", "开启通透模式", "通透模式开", "通透模式打开", "通透模式开启"
]

turn_transparency_mode_off = [
    "关闭通透模式", "取消通透模式", "通透模式关", "通透模式关闭", "通透模式取消"
]

################################################## Query Base for EQ ###################################################

increase_treble_level = [
    "调高高音", "高音调高", "调大高音", "高音调大", "增加高音", "高音增加",
    "增强高音", "高音增强", "高音加", "加高音", "高音太低了"
]

increase_mid_level = [
    "调高中音", "中音调高", "调大中音", "中音调大", "增加中音", "中音增加",
    "增强中音", "中音增强", "中音加", "加中音", "中音太低了"
]

increase_bass_level = [
    "调高低音", "低音调高", "调大低音", "低音调大", "增加低音", "低音增加",
    "增强低音", "低音增强", "低音加", "加低音", "低音太低了"
]

decrease_treble_level = [
    "调低高音", "高音调低", "调小高音", "高音调小", "减少高音", "高音减少",
    "减弱高音", "高音减弱", "高音减", "减高音", "高音太高了"
]

decrease_mid_level = [
    "调低中音", "中音调低", "调小中音", "中音调小", "减少中音", "中音减少",
    "减弱中音", "中音减弱", "中音减", "减中音", "中音太高了",
]

decrease_bass_level = [
    "调低低音", "低音调低", "调小低音", "低音调小", "减少低音", "低音减少",
    "减弱低音", "低音减弱", "低音减", "减低音", "低音太高了",
]

set_treble_level_to_max = [
    "调到最大高音", "高音调到最大", "调至最大高音", "高音调至最大", "设为最大高音", "高音设为最大",
    "加到最大高音", "高音加到最大", "升到最大高音", "高音升到最大", "最大高音", "高音最大"
]

set_mid_level_to_max = [
    "调到最大中音", "中音调到最大", "调至最大中音", "中音调至最大", "设为最大中音", "中音设为最大",
    "加到最大中音", "中音加到最大", "升到最大中音", "中音升到最大", "最大中音", "中音最大"
]

set_bass_level_to_max = [
    "调到最大低音", "低音调到最大", "调至最大低音", "低音调至最大", "设为最大低音", "低音设为最大",
    "加到最大低音", "低音加到最大", "升到最大低音", "低音升到最大", "最大低音", "低音最大"
]

set_treble_level_to_min = [
    "调到最小高音", "高音调到最小", "调至最小高音", "高音调至最小", "设为最小高音", "高音设为最小",
    "减到最小高音", "高音减到最小", "降到最小高音", "高音降到最小", "最小高音", "高音最小"
]

set_mid_level_to_min = [
    "调到最小中音", "中音调到最小", "调至最小中音", "中音调至最小", "设为最小中音", "中音设为最小",
    "加到最小中音", "中音加到最小", "升到最小中音", "中音升到最小", "最小中音", "中音最小"
]

set_bass_level_to_min = [
    "调到最小低音", "低音调到最小", "调至最小低音", "低音调至最小", "设为最小低音", "低音设为最小",
    "减到最小低音", "低音减到最小", "降到最小低音", "低音降到最小", "最小低音", "低音最小"
]

set_treble_level_to_default = [
    "高音调至默认值", "高音调为默认值", "高音设为默认值", "重置高音等级", "高音设为零", "高音清零", "清空高音等级"
]

set_mid_level_to_default = [
    "中音调至默认值", "中音调为默认值", "中音设为默认值", "重置中音等级", "中音设为零", "中音清零", "清空中音等级"
]

set_bass_level_to_default = [
    "低音调至默认值", "低音调为默认值", "低音设为默认值", "重置低音等级", "低音设为零", "低音清零", "清空低音等级"
]

set_treble_to_specific_level = ["高音设置为#", "高音设为#", "高音调至#", "高音调为#", "高音#", "高音#级", "#级高音"]

set_mid_to_specific_level = ["中音设置为#", "中音设为#", "中音调至#", "中音调为#", "中音#", "中音#级", "#级中音"]

set_bass_to_specific_level = ["低音设置为#", "低音设为#", "低音调至#", "低音调为#", "低音#", "低音#级","#级低音"]

set_multiple_eqs_to_specific_level = [
    ["高音#中音#", ["treble", "mid"]], ["高音#低音#", ["treble", "bass"]],
    ["中音#低音#", ["mid", "bass"]], ["高音#中音#低音#", ["treble", "mid", "bass"]]
]

########################################################################################################################
class Xiaowei_NC_Support:
    def __init__(self, dut, phone, source_nc, target_nc, query_nc_text, test_type):
        self.dut = dut
        self.phone = phone
        self.source_nc = source_nc
        self.target_nc = target_nc
        self.query_nc_text = query_nc_text
        self.test_type = test_type

    @property
    def get_nc_level(self):
        wait(1)
        self.current_nc_level = 10 - int(self.dut.status.get_cnc_level())
        return self.current_nc_level

    @property
    def check_nc_level(self):
        return self.target_nc == self.get_nc_level

    def adjust_nc_level(self):
        self.dut.device.set_cnc_level(10 - self.source_nc)

    @property
    def get_nc_state(self):
        wait(1)
        self.current_nc_state = int(self.dut.status.get_cnc_state())
        return self.current_nc_state

    @property
    def check_nc_state(self):
        return self.target_nc == self.get_nc_state

    def turn_nc_off(self):
        self.dut.device.turn_cnc_off(self.source_nc)
        self.source_nc_state = self.get_nc_state
        wait(2)

    def turn_nc_on(self):
        self.dut.device.turn_cnc_on(self.source_nc)
        self.source_nc_state = self.get_nc_state
        wait(2)

    def perform_nc_query(self):
        XiaoweiSupport.test_vpa(self.dut, self.query_nc_text, hold_seconds=6)
        return XiaoweiSupport.test_query_no_response()

    def get_query_nc_text_in_xw(self):
        return self.phone.xiaowei.verify_query_no_response_text(self.query_nc_text)

    def check_result(self):
        query_text_in_xw = self.get_query_nc_text_in_xw()
        if self.test_type == "nc_level":
            if self.check_nc_level and query_text_in_xw == self.query_nc_text:
                return [self.query_nc_text, query_text_in_xw, str(self.source_nc), str(self.current_nc_level), "PASS"]
            else:
                return [self.query_nc_text, query_text_in_xw, str(self.source_nc), str(self.current_nc_level), "FAIL"]
        else:
            if self.check_nc_state and query_text_in_xw == self.query_nc_text:
                return [self.query_nc_text, query_text_in_xw, str(self.source_nc_state), str(self.current_nc_state), "PASS"]
            else:
                return [self.query_nc_text, query_text_in_xw, str(self.source_nc_state), str(self.current_nc_state), "FAIL"]

class Xiaowei_EQ_Support:
    def __init__(self, dut, phone, source_eq_level, target_eq_level, query_eq_text, *args):
        self.dut = dut
        self.phone = phone
        self.source_eq_level = source_eq_level
        self.target_eq_level = target_eq_level
        self.query_eq_text = query_eq_text
        self.eq_types = args

    @property
    def get_eq_level(self):
        wait(3)
        return self.dut.status.get_eq_level()

    @property
    def check_eq_level(self):
        self.current_eq_level = self.get_eq_level

        if len(self.eq_types) == 1:
            # self.eq = self.eq_types[0]
            if self.eq_types[0] == "treble":
                self.current_treble_level = self.current_eq_level[2]
                self.current_eq_level = str(self.current_treble_level)
                return self.target_eq_level == self.current_treble_level
            if self.eq_types[0] == "mid":
                self.current_mid_level = self.current_eq_level[1]
                self.current_eq_level = str(self.current_mid_level)
                return self.target_eq_level == self.current_mid_level
            if self.eq_types[0] == "bass":
                self.current_bass_level = self.current_eq_level[0]
                self.current_eq_level = str(self.current_bass_level)
                return self.target_eq_level == self.current_bass_level

        if len(self.eq_types) == 2:
            # self.eq = self.eq_types[0] + "," + self.eq_types[1]
            if self.eq_types[0] == "treble" and self.eq_types[1] == "mid":
                self.current_treble_level = self.current_eq_level[2]
                self.current_mid_level = self.current_eq_level[1]
                self.current_eq_level = str(self.current_treble_level) + "," + str(self.current_mid_level)
                return self.target_eq_level == self.current_treble_level and self.target_eq_level == self.current_mid_level
            if self.eq_types[0] == "treble" and self.eq_types[1] == "bass":
                self.current_treble_level = self.current_eq_level[2]
                self.current_bass_level = self.current_eq_level[0]
                self.current_eq_level = str(self.current_treble_level) + "," + str(self.current_bass_level)
                return self.target_eq_level == self.current_treble_level and self.target_eq_level == self.current_bass_level
            if self.eq_types[0] == "mid" and self.eq_types[1] == "bass":
                self.current_mid_level = self.current_eq_level[1]
                self.current_bass_level = self.current_eq_level[0]
                self.current_eq_level = str(self.current_mid_level) + "," + str(self.current_bass_level)
                return self.target_eq_level == self.current_mid_level and self.target_eq_level == self.current_bass_level

        if len(self.eq_types) == 3:
            # self.eq = self.eq_types[0] + "," + self.eq_types[1] + "," + self.eq_types[2]
            if self.eq_types[0] == "treble" and self.eq_types[1] == "mid" and self.eq_types[2] == "bass":
                self.current_treble_level = self.current_eq_level[2]
                self.current_mid_level = self.current_eq_level[1]
                self.current_bass_level = self.current_eq_level[0]
                self.current_eq_level = str(self.current_treble_level) + "," + str(self.current_mid_level) + "," + str(self.current_bass_level)
                return self.target_eq_level == self.current_treble_level and self.target_eq_level == self.current_mid_level and self.target_eq_level == self.current_bass_level

    def adjust_eq_level(self):
        if len(self.eq_types) == 1:
            if self.eq_types[0] == "treble":
                self.dut.device.set_eq_level(self.source_eq_level, 2)
            if self.eq_types[0] == "mid":
                self.dut.device.set_eq_level(self.source_eq_level, 1)
            if self.eq_types[0] == "bass":
                self.dut.device.set_eq_level(self.source_eq_level, 0)

        if len(self.eq_types) == 2:
            if self.eq_types[0] == "treble" and self.eq_types[1] == "mid":
                self.dut.device.set_eq_level(self.source_eq_level, 2)
                self.dut.device.set_eq_level(self.source_eq_level, 1)
            if self.eq_types[0] == "treble" and self.eq_types[1] == "bass":
                self.dut.device.set_eq_level(self.source_eq_level, 2)
                self.dut.device.set_eq_level(self.source_eq_level, 0)
            if self.eq_types[0] == "mid" and self.eq_types[1] == "bass":
                self.dut.device.set_eq_level(self.source_eq_level, 1)
                self.dut.device.set_eq_level(self.source_eq_level, 0)

        if len(self.eq_types) == 3:
            if self.eq_types[0] == "treble" and self.eq_types[1] == "mid" and self.eq_types[2] == "bass":
                self.dut.device.set_eq_level(self.source_eq_level, 2)
                self.dut.device.set_eq_level(self.source_eq_level, 1)
                self.dut.device.set_eq_level(self.source_eq_level, 0)

    def perform_eq_query(self):
        # return XiaoweiSupport.test_xiaowei_vpa(self.dut, self.query_eq_text, hold_seconds=6, query_no_response=True)
        XiaoweiSupport.test_vpa(self.dut, self.query_eq_text, hold_seconds=6)
        return XiaoweiSupport.test_query_no_response()

    def get_query_eq_text_in_xw(self):
        return self.phone.xiaowei.verify_query_no_response_text(self.query_eq_text)

    def check_result(self):
        query_text_in_xw = self.get_query_eq_text_in_xw()
        if query_text_in_xw == self.query_eq_text:
            check_text = True
        else:
            correct_words_list = list(Matching_Table_of_Correct_Words_and_Wrong_Words)
            for correct_word in correct_words_list:
                if self.query_eq_text.find(correct_word) >= 0:
                    find_it = False
                    for wrong_word in Matching_Table_of_Correct_Words_and_Wrong_Words[correct_word]:
                        if query_text_in_xw.find(wrong_word) >= 0:
                            find_it = True
                            check_text = query_text_in_xw.replace(wrong_word, correct_word) == self.query_eq_text
                            break
                    if find_it:
                        break
            else:
                check_text = False

        if self.check_eq_level and check_text:
            return [self.query_eq_text, query_text_in_xw, (str(self.source_eq_level) + ",") * len(self.eq_types), self.current_eq_level, "PASS"]
        else:
            return [self.query_eq_text, query_text_in_xw, (str(self.source_eq_level) + ",") * len(self.eq_types), self.current_eq_level, "FAIL"]


