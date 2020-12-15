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
from wham_automation.test_scripts.Bamboo.lib.mobile.constants import HUAWEIConstant, XIAOMIConstant, OPPOConstant, VIVOConstant
from wham_automation.lib.framework.Configs.ProductInfo import Buttons
from wham_automation.script_support.AssertHelpers import SinkStates
from wham_automation.test_scripts.Bamboo.VPA_Xiaowei.Xiaowei_Support import VPAProcess
from appium.webdriver.common.touch_action import TouchAction

MAX_DUT_TO_SEARCH_IN_CAROUSEL = 2


class SettingsScenario(BasePage):
    pre_check_result = False

    def __initialize_variable_of_settings(self):
        """
        Initialize all variable used in this page
        :param:None
        :return:None
        :raises:None
        """

        if self.phone_info.phone_type == PhoneType.ANDROID:
            self.brand_scenario_dict = {'HUAWEI': HUAWEIConstant,
                                        'XIAOMI': XIAOMIConstant,
                                        'OPPO': OPPOConstant,
                                        'VIVO': VIVOConstant,
                                        }

            self.package_name = self.brand_scenario_dict[self.phone_info.brand].android_settings_app_package
            self.activity_name = self.brand_scenario_dict[self.phone_info.brand].android_settings_app_activity
            self.cellular_off_command = "adb shell svc data disable"
            self.cellular_on_command = "adb shell svc data enable"
            self.wifi_off_command = "adb shell svc wifi disable"
            self.wifi_on_command = "adb shell svc wifi enable"
            self.airplane_off_command = "adb shell settings put global airplane_mode_on 0"
            self.airplane_on_command = "adb shell settings put global airplane_mode_on 1"

        elif self.phone_info.phone_type == PhoneType.IOS:
            self.package_name = 'com.apple.Preferences'
            self.activity_name = 'com.apple.Preferences'
            self.airplane_mode_switch = '//XCUIElementTypeSwitch[@name="Airplane Mode"]'
            self.airplane_mode_switch_on = '//XCUIElementTypeSwitch[@name="Airplane Mode" and @value="1"]'
            self.airplane_mode_switch_off = '//XCUIElementTypeSwitch[@name="Airplane Mode" and @value="0"]'

            self.go_to_wifi_setting_screen = '//XCUIElementTypeStaticText[@value="WLAN"]'
            self.wifi_switch = '//XCUIElementTypeSwitch[@name="WLAN"]'
            self.wifi_switch_on = '//XCUIElementTypeSwitch[@name="WLAN" and @value="1"]'
            self.wifi_switch_off = '//XCUIElementTypeSwitch[@name="WLAN" and @value="0"]'

            self.go_to_cellular_setting_screen = '//XCUIElementTypeCell[@name="Cellular"]'
            self.cellular_switch = '//XCUIElementTypeSwitch[@name="Cellular Data"]'
            self.cellular_switch_on = '//XCUIElementTypeSwitch[@name="Cellular Data" and @value="1"]'
            self.cellular_switch_off = '//XCUIElementTypeSwitch[@name="Cellular Data" and @value="0"]'

        else:
            pass

    def launch_settings_app(self, driver=None):
        """
        Launch settings application
        :param:None
        :return:None
        :raises:None
        """
        status = ''
        is_application_launched = False
        self.__initialize_variable_of_settings()
        try:
            if driver:
                self.driver = driver
            else:
                self.driver = self.mobile_driver_factory_object.get_driver(
                    get_appium_server_ip(),
                    self.phone_info.appium_port,
                    self.phone_info.platform_name,
                    self.phone_info.os_version,
                    self.phone_info.config_name,
                    self.phone_info.uuid,
                    self.package_name,
                    self.activity_name,
                    self.phone_info.wda_local_port)
            wait(5, "To Settle Down App After Launching")
            is_application_launched = True
        except Exception as e:
            logger.error('Driver launch Fail on {}'.format(self.phone_info.bluetooth_name))
        return is_application_launched

    def go_to_test_screen(self, specific_xpath):
        try:
            logger.info("Prepare to go to test screen")
            self.driver.appium_driver.find_element_by_xpath(specific_xpath).click()
        except Exception as e:
            try:
                self.driver.appium_driver.back()
                logger.info("Prepare to go to test screen again")
                self.driver.appium_driver.find_element_by_xpath(specific_xpath).click()
            except Exception as e:
                logger.error("Unable to go to test screen")
                return False
            else:
                logger.info("Succeed to go to test screen")
                self.driver.appium_driver.back()
                return True
        else:
            logger.info("Succeed to go to test screen")
            return True

    def perform_setting(self, perform_setting_xpath):
        try:
            logger.info("Perform the required setting")
            wait(1)
            self.driver.appium_driver.find_element_by_xpath(perform_setting_xpath).click()
        except Exception as e:
            logger.error("Unable to do the required setting")
            return False
        else:
            logger.info("Complete the required setting")
            return True

    def verify_setting(self, check_setting_xpath):
        try:
            logger.info("Verify the required setting")
            self.driver.appium_driver.find_element_by_xpath(check_setting_xpath)
        except Exception as e:
            logger.error("The setting was verified to be wrong")
            return False
        else:
            logger.info("Complete the required setting successfully")
            return True

    def cellular_off(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            wait(4, "turn off cellular data")
            ret = subprocess.Popen(self.cellular_off_command, shell=True)
            ret.wait()
            if ret.returncode == 0:
                return True
            else:
                return False
        else:
            if self.go_to_test_screen(self.go_to_cellular_setting_screen):
                if self.verify_setting(self.cellular_switch_off):
                    self.driver.appium_driver.back()
                    return True
                else:
                    if self.perform_setting(self.cellular_switch):
                        if self.verify_setting(self.cellular_switch_off):
                            self.driver.appium_driver.back()
                            return True
                        else:
                            self.driver.appium_driver.back()
                            return False
                    else:
                        self.driver.appium_driver.back()
                        return False
            else:
                self.driver.appium_driver.back()
                return False

    def cellular_on(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            ret = subprocess.Popen(self.cellular_on_command, shell=True)
            ret.wait()
            if ret.returncode == 0:
                return True
            else:
                return False
        else:
            if self.go_to_test_screen(self.go_to_cellular_setting_screen):
                if self.verify_setting(self.cellular_switch_on):
                    self.driver.appium_driver.back()
                    return True
                else:
                    if self.perform_setting(self.cellular_switch):
                        wait(2)
                        if self.verify_setting(self.cellular_switch_on):
                            self.driver.appium_driver.back()
                            return True
                        else:
                            self.driver.appium_driver.back()
                            return False
                    else:
                        self.driver.appium_driver.back()
                        return False
            else:
                self.driver.appium_driver.back()
                return False

    def wifi_off(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            wait(3, "turn off wifi")
            ret = subprocess.Popen(self.wifi_off_command, shell=True)
            ret.wait()
            if ret.returncode == 0:
                return True
            else:
                return False
        else:
            if self.go_to_test_screen(self.go_to_wifi_setting_screen):
                if self.verify_setting(self.wifi_switch_off):
                    self.driver.appium_driver.back()
                    return True
                else:
                    if self.perform_setting(self.wifi_switch):
                        if self.verify_setting(self.wifi_switch_off):
                            self.driver.appium_driver.back()
                            return True
                        else:
                            self.driver.appium_driver.back()
                            return False
                    else:
                        self.driver.appium_driver.back()
                        return False
            else:
                self.driver.appium_driver.back()
                return False

    def wifi_on(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            ret = subprocess.Popen(self.wifi_on_command, shell=True)
            ret.wait()
            if ret.returncode == 0:
                return True
            else:
                return False
        else:
            if self.go_to_test_screen(self.go_to_wifi_setting_screen):
                if self.verify_setting(self.wifi_switch_on):
                    self.driver.appium_driver.back()
                    return True
                else:
                    if self.perform_setting(self.wifi_switch):
                        wait(2)
                        if self.verify_setting(self.wifi_switch_on):
                            self.driver.appium_driver.back()
                            return True
                        else:
                            self.driver.appium_driver.back()
                            return False
                    else:
                        self.driver.appium_driver.back()
                        return False
            else:
                self.driver.appium_driver.back()
                return False

    def airplane_off(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            wait(4, "turn off airplane mode")
            ret = subprocess.Popen(self.airplane_off_command, shell=True)
            ret.wait()
            if ret.returncode == 0:
                return True
            else:
                return False
        else:
            if self.verify_setting(self.airplane_mode_switch_off):
                return True
            else:
                if self.perform_setting(self.airplane_mode_switch):
                    if self.verify_setting(self.airplane_mode_switch_off):
                        return True
                    else:
                        return False
                else:
                    return False

    def airplane_on(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            wait(4, "turn on airplane mode")
            ret = subprocess.Popen(self.airplane_on_command, shell=True)
            ret.wait()
            if ret.returncode == 0:
                return True
            else:
                return False
        else:
            if self.verify_setting(self.airplane_mode_switch_on):
                return True
            else:
                if self.perform_setting(self.airplane_mode_switch):
                    if self.verify_setting(self.airplane_mode_switch_on):
                        return True
                    else:
                        return False
                else:
                    return False

    def activate_app(self):
        logger.info('The settings app will be brought to foreground')
        try:
            self.driver.appium_driver.activate_app(self.package_name)
        except Exception as e:
            logger.error(e)
            logger.info('The settings app cannot be brought to foreground')
            return False
        else:
            logger.info('The settings app has been brought to foreground successfully')
            return True

    def close_app(self):
        logger.info('The settings app will be closed')
        try:
            self.driver.appium_driver.close_app()
        except Exception as e:
            logger.error(e)
            logger.info('The settings app cannot be closed')
            return False
        else:
            logger.info('The settings app has been closed successfully')
            return True

    def terminate_app(self):
        logger.info('The settings app will be terminated')
        try:
            self.driver.appium_driver.terminate_app(self.package_name)
        except Exception as e:
            logger.info('The settings app cannot be terminated')
        else:
            logger.info('The settings app has been terminated successfully')
        return True
