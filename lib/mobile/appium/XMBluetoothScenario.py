# -*- coding  utf-8 -*-
#
#  Organization  BOSE CORPORATION
#  Copyright     COPYRIGHT 2019 BOSE CORPORATION ALL RIGHTS RESERVED.
#                This program may not be reproduced, in whole or in part in any
#                form or any means whatsoever without the written permission of
#                    BOSE CORPORATION
#                    The Mountain,
#                    Framingham, MA 01701-9168
#
###############################################################################
"""
Scenario that is used to Perform Various Bluetooth operation on Connected Mobile devices.
@author          einfochips
@date            Creation Date: 21/07/2017
"""

import time
from time import sleep
import sys
import subprocess
from wham_automation.script_support.ScriptHelper import wait
from wham_automation.lib.framework.Configs.FrameworkConstants import PhoneType
from wham_automation.lib.mobile.scenario.bluetooth_interface import BluetoothInterface
from wham_automation.utils.ConfigParser import \
    get_android_settings_app_package, get_android_settings_app_activity, \
    logger, get_ios_settings_bundle_id, get_ios_settings_app_package, \
    get_appium_server_ip
from wham_automation.lib.mobile.scenario.BasePage import BasePage
from wham_automation.lib.mobile.constants import IosPhoneConstant
from wham_automation.test_scripts.Bamboo.lib.mobile.constants import XIAOMIConstant
from wham_automation.lib.mobile.scenario.PhoneInfo import PhoneInfo


class XMBluetoothScenario(BasePage, BluetoothInterface):
    def __init__(self, android_locators=XIAOMIConstant,
                 ios_locators=IosPhoneConstant,
                 phone_info: PhoneInfo = None):
        super().__init__(android_locators=android_locators, ios_locators=ios_locators, phone_info=phone_info)

    @staticmethod
    def button_is_on(button):
        if type(button.text) is bool:
            return button.text
        if button.get_attribute("checked").lower() == "false":
            return False
        if button.get_attribute("checked").lower() == "true":
            return True

        return button.text.lower() == 'on' or button.text == '1'

    @staticmethod
    def is_switch_on(switch):
        if type(switch.text) is bool:
            return switch.text

        return switch.text.lower() == 'on' or switch.text.lower() == 'true' or switch.text == '1'

    def _get_android_phone_model(self):
        try:
            command_to_get_model_number = 'adb -s {} shell getprop ' \
                                          'ro.product.model'\
                .format(self.phone_info.uuid)
            if sys.platform == 'win32':
                command_to_get_model_number = 'cmd', '/c', 'adb -s {} shell getprop ro.product.model'.\
                    format(self.phone_info.uuid)
            model_number = subprocess.check_output(
                command_to_get_model_number,
                shell=True)
            model_name = str(model_number.decode().splitlines()).upper()
            return model_name
        except Exception as ex:
            # log error and return blank mode number
            logger.debug(ex)
            return ""

    def __initialize_variable_of_bluetooth(self):
        """
        Initialize all variable used in this page
        :param:None
        :return:None
        :raises:None
        """
        if self.phone_info.phone_type == PhoneType.ANDROID:
            self.package_name = XIAOMIConstant.bluetooth_settings_app_package
            self.activity_name = XIAOMIConstant.bluetooth_app_activity
            self.bluetooth_button_on_off_button = 'self.android_locators.BLUETOOTH_ON_OFF_ByID'
            self.bluetooth_button = 'self.android_locators.BLUETOOTH_BUTTON_ByXPATH'
            self.bluetooth_on_off_check = 'self.android_locators.BLUETOOTH_ON_OFF_CHECK_ByXPATH'
            self.paired_devices_show_more_less = 'self.android_locators.PAIRED_DEVICES_SHOW_MORE_LESS_ByID'
            self.paired_device_text = 'self.android_locators.PAIRED_DEVICE_TEXT_ByXPATH'
            self.paired_device_list = 'self.android_locators.BLUETOOTH_PAIRED_DEVICE_LIST_ByXPATH'
            self.bluetooth_pair_device = 'self.android_locators.BLUETOOTH_CONNECT_DEVICE_ByXPATH'

            self.bluetooth_pair_new_device_refresh_button = \
                'self.android_locators.BLUETOOTH_PAIR_NEW_DEVICE_REFRESH_ByXPATH'
            self.bluetooth_contact_access_allow_button = 'self.android_locators.BLUETOOTH_CONTACT_ACCESS_ALLOW_BUTTON_ByXPATH'
            self.bluetooth_pair_button = 'self.android_locators.BLUETOOTH_PAIR_BUTTON_ByXPATH'
            self.bluetooth_cancel_pair_button = 'self.android_locators.BLUETOOTH_CANCEL_PAIR_BUTTON_ByXPATH'
            self.bluetooth_pair_failed_button = 'self.android_locators.BLUETOOTH_PAIR_FAILED_BUTTON_ByXPATH'
            self.bluetooth_device_name_cancel_button = 'self.android_locators.BLUETOOTH_DEVICE_NAME_CANCEL_BUTTON_ByXPATH'
            self.bluetooth_pair_device_with_title = 'self.android_locators.BLUETOOTH_CONNECT_DEVICE_WITH_TITLE_ByXPATH'

            self.bluetooth_paired_device_list = \
                'self.android_locators.BLUETOOTH_AVAILABLE_DEVICE_LIST_ByXPATH'
            self.bluetooth_connection_status = \
                'self.android_locators.BLUETOOTH_CONNECTION_STATUS_ByXPATH'
            self.bluetooth_connected_device_list = \
                'self.android_locators.BLUETOOTH_CONNECTED_DEVICE_LIST_ByXPATH'
            self.bluetooth_discovered_device_list = \
                'self.android_locators.BLUETOOTH_LIST_OF_AVAILABLE_DEVICES_ByXPATH'
            self.bluetooth_settings_button = \
                'self.android_locators.BLUETOOTH_CONNECTION_SETTINGS_ByID'
            self.bluetooth_not_connected_device = \
                'self.android_locators.BLUETOOTH_CONNECTED_DEVICE_LIST_ByXPATH'
            self.bluetooth_more_options_button = \
                'self.android_locators.BLUETOOTH_MORE_OPTIONS_ByXPATH'
            self.device_name = \
                'self.android_locators.BLUETOOTH_RENAME_BUTTON_ByXPATH'
            self.device_name_text_box = \
                'self.android_locators.BLUETOOTH_EDIT_TEXTBOX_ByID'
            self.set_name_button = \
                'self.android_locators.BLUETOOTH_SET_NAME_BUTOON_ByXPATH'
            self.bluetooth_mac_addess = \
                'self.android_locators.BLUETOOTH_MAC_ADDRESS_ByXPATH'
            self.general_button_settings = \
                'self.android_locators.ABOUT_PHONE_BUTTON_ByXPATH'
            self.status_button = 'self.android_locators.STATUS_BUTTON_ByXPATH'
            self.contact_sharing_button = \
                'self.android_locators.BLUETOOTH_ENABLE_CONTACT_SHARING_BUTTON_ByXPATH'
            self.contact_sharing_confirmation_ok_button = \
                'self.android_locators.BLUETOOTH_ENABLE_CONTACT_SHARING_CONFIRM_OK_BUTTON_ByXPATH'
            self.device_to_connect_after_swipe = \
                'self.android_locators.BLUETOOTH_DEVICE_TO_CONNECT_AFTER_SWIPE_ByID'
            self.pop_up_ok_button = \
                'self.android_locators.BLUETOOTH_POP_UP_OK_BUTTON_ByXPATH'
            self.connected_device_button = \
                'self.android_locators.CONNECTED_DEVICES_BUTTON_ByXPATH'
            self.connection_references = \
                'self.android_locators.CONNECTION_REFERENCES_BUTTON_ByXPATH'
            self.bluetooth_device_setting_button = \
                'self.android_locators.BLUETOOTH_DEVICE_SETTINGS_BUTTON_ByID'
            if (self.phone_info.os_version.startswith('6.')) or '8.0.0' in self.phone_info.os_version:
                # Special override for 6.X phones. Fixes my Nexus 6P/Android
                #  6.0.1 phone. Not sure about any others...
                # TODO: Once we get a way to figure out a phone's model,
                # make the Android 8.0.0 check *not* apply to the Nexus 6P.
                # Looks like the above now is also used on Android 8.0.0. As
                #  far as I can tell this breaks the Nexus 6P...
                # But, based on the commit history, I think this was added
                # for the Samsung phones.
                self.bluetooth_device_setting_button = \
                    'self.android_locators.BLUETOOTH_DEVICE_SETTINGS_BUTTON_6_0_1_ByID'
            self.contact_sharing_checkbox = \
                'self.android_locators.BLUETOOTH_ENABLE_CONTACT_SHARING_CHECKBOX_ByXPATH'
            self.media_sharing_switch = \
                'self.android_locators.BLUETOOTH_MEDIA_SHARING_SWITCH_ByXPATH'
            self.media_sharing_button = \
                'self.android_locators.BLUETOOTH_ENABLE_DISABLE_MEDIA_SHARING_ByXPATH'
            self.bluetooth_pair_new_device_in_android_8_1_button = \
                'self.android_locators.BLUETOOTH_ADD_NEW_DEVICE_IN_8_1_ByXPATH'
            self.contact_sharing_button_in_android_8_1_switch = \
                'self.android_locators.BLUETOOTH_ENABLE_CONTACT_SHARING_SWITCH_IN_8_1_ByXPATH'
            self.pop_up_ok_button = \
                'self.android_locators.BLUETOOTH_POP_UP_OK_BUTTON_ByXPATH'
            self.bluetooth_status_summary = \
                'self.android_locators.BLUETOOTH_STATUS_SUMMARY_ByXPATH'
            self.previously_paired_device_button = \
                'self.android_locators.BLUETOOTH_PREVIUSLY_CONNECTED_DEVICE_BUTTON_ByXPATH'
            self.bluetooth_more_options = \
                'self.android_locators.SAMSUNG_CONTACT_MORE_DETAILS_ByXPATH'
            self.media_volume_text = \
                'self.android_locators.BLUETOOTH_MEDIA_VOLUME_SYNC_ByXPATH'
            self.media_volume_sync_switch = \
                'self.android_locators.BLUETOOTH_VOLUME_SYNC_SWITCH_ByID'

        elif self.phone_info.phone_type == PhoneType.IOS:
            self.package_name = get_ios_settings_bundle_id()
            self.activity_name = get_ios_settings_app_package()
            self.bluetooth_button_on_off_button = \
                'self.ios_locators.BLUETOOTH_ON_OFF_BUTTON_ByXPATH'
            self.bluetooth_button = 'self.ios_locators.BLUETOOTH_ByXPATH'
            self.paired_device_list = \
                'self.ios_locators.BLUETOOTH_IS_PAIRED_DEVICE_LIST_ByXPATH'
            self.bluetooth_connection_status = \
                'self.ios_locators.BLUETOOTH_VERIFY_DEVICE_CONNECTED_ByXPATH'
            self.bluetooth_connected_device_list = \
                'self.ios_locators.BLUETOOTH_LIST_OF_CONNECTED_DEVICES_ByXPATH'
            self.bluetooth_discovered_device_list = \
                'self.ios_locators.BLUETOOTH_LIST_OF_SCANNED_DEVICES_ByXPATH'
            self.bluetooth_paired_device_list = \
                'self.ios_locators.BLUETOOTH_IS_PAIRED_DEVICE_LIST_ByXPATH'
            self.bluetooth_pair_device = \
                'self.ios_locators.BLUETOOTH_DEVICES_LIST_ByXPATH'
            self.paired_device_list = \
                'self.ios_locators.BLUETOOTH_IS_PAIRED_DEVICE_LIST_ByXPATH'
            self.bluetooth_settings_button = \
                'self.ios_locators.BLUETOOTH_MORE_INFO_BUTTON_ByXPATH'
            self.bluetooth_not_connected_device = \
                'self.ios_locators.BLUETOOTH_LIST_OF_NOT_CONNECTED_DEVICES_ByXPATH'
            self.general_button_settings = \
                'self.ios_locators.GENERAL_BUTTON_ByXPATH'
            self.status_button = 'self.ios_locators.ABOUT_BUTTON_ByXPATH'
            self.device_name = 'self.ios_locators.NAME_BUTTON_ByXPATH'
            self.device_name_text_box = \
                'self.ios_locators.DEVICE_NAME_TEXTFIELD_ByXPATH'
            self.set_name_button = 'self.ios_locators.DONE_BUTTON_ByXPATH'
            self.bluetooth_mac_addess = \
                'self.ios_locators.BLUETOOTH_MAC_ADDRESS_ByXPATH'
            self.device_to_connect_after_swipe = \
                'self.ios_locators.BLUETOOTH_DEVICE_TO_CONNECT_AFTER_SWIPE_ByXPATH'
            self.contact_sharing_button = \
                'self.ios_locators.CONTACT_SHARING_SWITCH_ByXPATH'
            self.bluetooth_device_setting_button = \
                'self.ios_locators.BLUETOOTH_DEVICE_SETTINGS_BUTTON_ByID'
            self.pop_up_ok_button = \
                'self.ios_locators.BLUETOOTH_POP_UP_OK_BUTTON_ByXPATH'

    def _go_to_connected_device_screen(self, no_of_back_click=1):
        if self.phone_info.phone_type == PhoneType.ANDROID and self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
            for _ in range(no_of_back_click):
                self.driver.appium_driver.back()

    def __verify_current_screen(self):
        """
        verify current screen
        :param:None
        :return:
            is_bluetooth_button__visible: True = Bluetooth button is
            visible, False = Bluetooth button is not visible
        :raises:None
        """
        is_bluetooth_button_visible = False
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_cancel_pair_button, 1)
        except Exception as e:
            logger.warning("No cancel paired button pops up")
        else:
            sleep(1)
            self.find_element(self.driver.appium_driver,
                              self.bluetooth_cancel_pair_button, 0).click()

        try:
            sleep(3)  # Added Static sleep as is_display=False for iOS
            # 11.3.wait_till_element visible will not work.
            is_bluetooth_button_visible = self.find_element(
                self.driver.appium_driver, self.bluetooth_on_off_check,
                0).is_enabled()
        except:
            logger.debug("Bluetooth On/OFF Button is currently not visible")
        return is_bluetooth_button_visible

    def launch_settings(self, driver=None):
        """
        Launch settings application
        :param:None
        :return:None
        :raises:None
        """
        status = ''
        is_application_launched = False
        self.__initialize_variable_of_bluetooth()
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
            logger.error('Driver launch Fail on {}'.format(
                self.phone_info.bluetooth_name))
            logger.error(repr(e))
        return is_application_launched

    def _go_to_bluetooth_button(self):
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_button, 10)
            self.find_element(self.driver.appium_driver, self.bluetooth_button,
                              1).click()
            logger.debug('Go to bluetooth on/off switch screen from Settings')
        except Exception as e:
            logger.warning("Bluetooth Button not visible")

    def bt_radio(self, enable='on'):
        """
        enable or disable bt as per user input.
        :param: enable (str) : on if you want to enable Bluetooth radio
        :return:is_radio_on(boolean): True if action performed, False otherwise
        :raises:None
        """
        is_radio_on = False
        turn_on = True
        if enable.lower() == 'off':
            turn_on = False
        bt_status = self.__verify_current_screen()
        try:
            logger.debug("Current Bluetooth Status is {}". format(bt_status))
            bluetooth_on_off_switch = self.find_element(
                self.driver.appium_driver,
                self.bluetooth_button_on_off_button, 0)
            is_radio_on = self._toggle_switch(bluetooth_on_off_switch, turn_on)
            self._click_ok_popup_after_bluetooth_off()

        except Exception as e:
            self.take_screenshot(self.driver.appium_driver, 'bt_radio')
            logger.warning('Bluetooth button is not visible')
            logger.warning(repr(e))
        return is_radio_on

    def _click_ok_popup_after_bluetooth_off(self):
        if self.phone_info.phone_type == PhoneType.IOS:
            try:
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     'self.ios_locators.OK_BUTTON_AFTER_BLUETOOTH_OFF_ByID',
                                                     3)
                self.find_element(self.driver.appium_driver,
                                  'self.ios_locators.OK_BUTTON_AFTER_BLUETOOTH_OFF_ByID',
                                  0).click()
            except:
                logger.warning("OK POPUP AFTER BLUETOOTH OFF IS NOT VISIBLE")

    def bt_radio_fast(self, turn_on):
        """
        A clone of bt_radio() except simplified to be faster.
        Shouldn't do anything if we're already in the right state.

        :param turn_on: A boolean value indicating if the radio should be
        turned on. (If false, will turn the radio off.)
        """
        assert turn_on in {True,
                           False}, "The 'turn _on' argument must be True or " \
                                   "False. Given: {!r}".format(turn_on)
        # Get the Bluetooth button (and guarantee we're on the right screen).
        try:
            sleep(
                2)  # Added Static sleep as is_display=False for iOS
            # 11.3.wait_till_element visible will not work.
            bluetooth_element = self.find_element(self.driver.appium_driver,
                                                  self.bluetooth_button_on_off_button,
                                                  0)
            assert bluetooth_element is not None
        except:
            self._go_to_bluetooth_button()
            # TODO: 15 seconds seems a bit long?
            sleep(
                2)  # Added Static sleep as is_display=False for iOS
            # 11.3.wait_till_element visible will not work.
            bluetooth_element = self.find_element(self.driver.appium_driver,
                                                  self.bluetooth_button_on_off_button,
                                                  0)
            assert bluetooth_element is not None, "Couldn't find the " \
                                                  "bluetooth on/off switch " \
                                                  "after using " \
                                                  "_go_to_bluetooth_button()!"
        # Now click that button if we're in the wrong state.
        radio_is_on = self.button_is_on(bluetooth_element)
        if turn_on != radio_is_on:
            logger.debug(
                "For phone {!r}, found that Bluetooth is currently {}. "
                "Toggling so will be {}.".format(
                    self.phone_info.bluetooth_name,
                    "ON" if radio_is_on else "OFF",
                    "ON" if turn_on else "OFF",
                ))

            # Make absolutely sure the switch is still visible. Need this as
            #  I've seen instances where the "Setup your Google Assistant"
            # menu drops down over this button (and clicking on it causes us
            #  to open the Google Assistant setup menu instead).
            # NOTE: I can't seem to wait for this element to disappear,
            # so I'm going to manually wait for it to stop being findable
            # instead...
            self.wait_for_google_assistant_pop_up_to_disappear()
            # Then click it.
            bluetooth_element.click()
            self._click_ok_popup_after_bluetooth_off()
        else:
            logger.debug(
                "For phone {!r}, found that Bluetooth is already {}. Leaving "
                "it that way.".format(
                    self.phone_info.bluetooth_name,
                    "ON" if radio_is_on else "OFF",
                ))
        self._go_to_connected_device_screen(no_of_back_click=2)

    def bt_enabled(self):
        """
        Get current status of bluetooth
        :param:None
        :return:
            is_bt_enabled (str) : True if bluetooth is enabled, False otherwise
        :raises:None
        """
        is_bt_enabled = False

        self.check_if_bt_pairing_fail()

        self.__verify_current_screen()

        try:
            logger.debug("Get Current Bluetooth Status")
            sleep(2)
            bluetooth_status = self.find_element(self.driver.appium_driver,
                                                 self.bluetooth_on_off_check,
                                                 0)
            if self.button_is_on(bluetooth_status):
                logger.debug("Bluetooth Status of {} is ON".format(
                    self.phone_info.bluetooth_name))
                is_bt_enabled = True
            else:
                logger.debug("Bluetooth Status of {} is OFF".format(
                    self.phone_info.bluetooth_name))
                is_bt_enabled = False
        except Exception as e:
            logger.warning('Bluetooth Button is not visible')
            logger.warning(repr(e))
            # raise

        return is_bt_enabled

    def check_if_bt_pairing_fail(self):
        """
        Check if exist bluetooth pairing failed window in current page
        :param:None
        """
        logger.info("Get Current pairing Status")

        sleep(2)
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_pair_failed_button, 5)
        except Exception as e:
            logger.warning('There is no bluetooth pairing failed window')
            return False
        else:
            logger.warning('There is bluetooth pairing failed window, click OK button to quit the window')
            sleep(1)
            self.find_element(self.driver.appium_driver,
                              self.bluetooth_pair_failed_button, 1).click()
            return True

    def _go_to_bt_paired_android_9_screen(self):
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.connected_device_button,
                                                 10)
            self.find_element(self.driver.appium_driver,
                              self.connected_device_button, 0).click()
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.previously_paired_device_button,
                                                 10)
            previously_connected_device_button = self.find_element(
                self.driver.appium_driver,
                self.previously_paired_device_button, 0).is_enabled()
            if not previously_connected_device_button:
                logger.warning(
                    "Currently no bluetooth device is paired with mobile")
                return False

            self.find_element(self.driver.appium_driver,
                              self.previously_paired_device_button, 0).click()
            return True
        except Exception as e:
            logger.warning("Need to attempt pair before is_paired")
            logger.warning(repr(e))
            return False

    def bt_is_paired(self):
        """
        Checks if the phone is paired with the last address we attempted
        a pairing operation with. To be used directly after pair(mac) or
        unpair(mac).
        :param:None
        :return:
            is_paired (boolean) : True, False (True = Paired, False = Not
            paired)
        :raise:None
        """
        is_paired = False
        try:
            # self.show_more_for_paired_devices()
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.paired_device_list, 5)
            pair_device_list = self.find_elements(self.driver.appium_driver,
                                                  self.paired_device_list, 0)

            logger.debug('Checks if the phone is paired with the any devices')
            if len(pair_device_list) > 0:
                if pair_device_list[0].text.upper() == "PAIR NEW DEVICE":
                    return False

                logger.debug(
                    "phone {} paired with some bluetooth device".format(
                        self.phone_info.bluetooth_name))
                is_paired = True

        except Exception as e:
            logger.warning("Need to attempt pair before is_paired")
        return is_paired

    def bt_is_connected(self):
        """
        Tests if phone is connected to something
        :param:None
        :returns
         (boolean) : True, False (True = connected, False = disconnected)
        :raises:None
        """
        try:
            is_bluetooth_on = self.bt_enabled()

            # if bluetooth is OFF then throw Exception
            if not is_bluetooth_on:
                logger.error("The bluetooth is disabled on {}".format(self.phone_info.bluetooth_name))

                self.bt_radio("on")
                # return False
                # sys.exit(0)

            # displays all paired devices
            # self.show_more_for_paired_devices()

            bluetooth_connected_device_list = self.find_elements(
                self.driver.appium_driver,
                self.bluetooth_connected_device_list, 0)

            time.sleep(1)
            if len(bluetooth_connected_device_list) > 0:
                logger.debug(
                    "phone {} is connected with some bluetooth device".format(
                        self.phone_info.bluetooth_name))
                return True
        except Exception as e:
            logger.warning(
                "Need to attempt connect before checking connection status.")

            logger.warning(repr(e))
            # raise
        return False

    def show_more_for_paired_devices(self):
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.paired_devices_show_more_less,
                                                 1)
        except Exception as e:
            logger.debug("No show more or show less button on the phone.")
        else:
            try:
                paired_devices_show_more_less = self.find_element(self.driver.appium_driver,
                                                                  self.paired_devices_show_more_less, 0)
                if paired_devices_show_more_less.text.lower() == 'show more':
                    paired_devices_show_more_less.click()
            except Exception as e:
                logger.warning(
                    "failed to display all paired devices.")
                logger.warning(repr(e))

    def bt_is_paired_to(self, paired_bluetooth_device):
        """
        Check if the phone is paired with a specific device.
        :param:
            paired_bluetooth_device (str) : Name of mobile device
        :return:
          is_paired_with_device (boolean) : True if paired with the device,
          False otherwise.
        :raise:
            None
        """
        is_paired_with_device = False
        try:
            bt_is_paired = self.bt_is_paired()
            if not bt_is_paired:
                return is_paired_with_device

            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.paired_device_list, 10)
            pair_element = self.find_elements(self.driver.appium_driver,
                                              self.paired_device_list, 0)

            for index in range(len(pair_element)):
                if self.is_same_bluetooth_name(pair_element[index],
                                               paired_bluetooth_device):
                    is_paired_with_device = True
                    break
        except Exception as e:
            logger.warning("Need to attempt pair or unpair before is_paired.")
            logger.warning(repr(e))
            # raise
        return is_paired_with_device

    def _get_bluetooth_paired_device_list(self, paired_device_list):
        paired_bluetooth_device_list = []
        paired_list = []
        if paired_device_list is not None:
            for index in range(len(paired_device_list)):
                element_text = paired_device_list[index].text
                if type(element_text) is not str:
                    logger.warn(
                        "Found pairing list element's text was None! "
                        "Ignoring for now.")
                    continue
                if element_text.strip() != "Connected":
                    if 'Visible' not in element_text:
                        paired_bluetooth_device_list.append(
                            str(element_text).strip())
            paired_list = list(
                filter(None, paired_bluetooth_device_list))  # fastest
            logger.debug("List of Paired Devices:{}".format(paired_list))
            return paired_list

    def bt_get_pairlist(self):
        """
        Gets the current list of paired devices.
        :param:None
        :return:
            paired_bluetooth_device_list(List) : list of all paired devices
        :raise:None
        """
        bluetooth_paired_device_list = []
        try:
            bt_is_paired = self.bt_is_paired()
            if bt_is_paired is False:
                return bluetooth_paired_device_list

            logger.debug('Get list of paired bluetooth devices:')
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_paired_device_list,
                                                 10)

            paired_device_lists_text = self.find_elements(self.driver.appium_driver,
                                                          self.paired_device_text,
                                                          0)

            bluetooth_paired_device_list = \
                self._get_bluetooth_paired_device_list(paired_device_lists_text)

        except Exception as e:
            logger.warning("Need to attempt pair before bt_get_pairlist.")
            logger.warning(repr(e))
            # raise
        return bluetooth_paired_device_list

    def bt_get_connected_devices(self):
        """
        Get list of connected blutooth devices on given mobile device
        :param:None
        :return:
            connected_bluetooth_device_list (List) : List of all connected
            bluetooth devices
        :raise:None
        """
        connected_bluetooth_device_list = []
        try:
            bt_is_connected = self.bt_is_connected()
            if bt_is_connected is False:
                logger.debug("No bluetooth device are connected")
                return connected_bluetooth_device_list

            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_connected_device_list,
                                                 10)
            element_list = self.find_elements(self.driver.appium_driver,
                                              self.bluetooth_connected_device_list,
                                              1)

            # To add connected bluetooth device name in list
            for index in range(len(element_list)):
                connected_bluetooth_device_list.append(
                    str(element_list[index].text.replace('\u200e', '')))
            logger.debug("List of Connected Devices:" + str(
                connected_bluetooth_device_list))
        except Exception as e:
            logger.warning(
                "Need to attempt connect before get_connected_devices.")
            logger.warning(repr(e))
        # self._go_to_connected_device_screen(no_of_back_click=1)
        return connected_bluetooth_device_list

    def bt_get_discovered_devices(self):
        """
        Get list of discovered blutooth devices on  mobile device
        :param:None
        :return:
            discovered_bluetooth_device_list (List) : List of all discovered
            bluetooth devices
        :raise:None
        """
        discovered_bluetooth_device = []
        try:
            self.bt_radio('on')
            if '8.1' in self.phone_info.os_version:
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.bluetooth_pair_new_device_in_android_8_1_button,
                                                     10)
                self.find_element(self.driver.appium_driver,
                                  self.bluetooth_pair_new_device_in_android_8_1_button,
                                  2).click()
            time.sleep(10)
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_discovered_device_list,
                                                 10)
            element_list = self.find_elements(self.driver.appium_driver,
                                              self.bluetooth_discovered_device_list,
                                              1)

            # To add connected bluetooth device name in list
            for index in range(len(element_list)):
                discovered_bluetooth_device.append(
                    str(element_list[index].text.replace('\u200e', '')))
            logger.debug("List of Discovered Devices:" + str(
                discovered_bluetooth_device))
        except Exception as e:
            self.take_screenshot(self.driver.appium_driver,
                                 '__retry_to_bt_connect')
            logger.error("No device are discoverable .")
            logger.error(repr(e))
        return discovered_bluetooth_device

    def bt_unpair(self, device_name_to_unpair):
        """
        Initiates a pair to a selected bluetooth device.
        To check if this pair succeeded, use is_paired().
        To check if any device is paired currently, use is_paired_with(mac)
        It is recommended to use pair_and_check(mac) instead.
        :param:
            device_name_to_unpair (str) : Bluetooth device name that you
            want to unpair
        :return:
            is_bluetooth_unpaired (boolean) = True if device unpaired.False
            otherwise
        :raise:None

        """
        is_bluetooth_unpaired = False
        try:
            is_device_paired = self.bt_is_paired()
            if is_device_paired is False:
                return True

            logger.debug('Unpair Paired {} Bluetooth device'.format(
                device_name_to_unpair))

            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.paired_device_list, 10)

            self.find_element(self.driver.appium_driver,
                              self.paired_device_list, 0).click()

            try:
                self.wait_till_element_to_be_visible(
                    self.driver.appium_driver,
                    'self.android_locators.BLUETOOTH_UNPAIR_BUTTON_ByXPATH',
                    10)
                self.find_element(self.driver.appium_driver,
                                  'self.android_locators.BLUETOOTH_UNPAIR_BUTTON_ByXPATH',
                                  0).click()
            except Exception as e:
                logger.debug(
                    "Unpair text not visible on Connected phone {} "
                    "".format(
                              (self.phone_info.bluetooth_name)))

            is_bluetooth_unpaired = True

        except Exception as e:
            self.take_screenshot(self.driver.appium_driver, 'bt_unpair')
            logger.warning("Need to attempt pair before unpair")
            logger.warning(repr(e))
        return is_bluetooth_unpaired

    def bt_start_discovery(self):
        """
        Start  Bluetooth discovery on phone
        :param:None
        :return:
            is_stop_discovery (boolean) :True = Bt is in discovery mode,
            False otherwise
        :raise:None
        """
        is_start_discovery = False
        try:
            is_bluetooth_on = self.bt_radio('on')
            if '8.1' in self.phone_info.os_version:
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.bluetooth_pair_new_device_in_android_8_1_button,
                                                     10)
                self.find_element(self.driver.appium_driver,
                                  self.bluetooth_pair_new_device_in_android_8_1_button,
                                  2).click()
                is_bluetooth_on = True
            if is_bluetooth_on:
                logger.debug("Bluetooth discovery Stared on {}".format(
                    self.phone_info.bluetooth_name))
                is_start_discovery = True
            else:
                logger.debug("Bluetooth discovery not Stared on {}".format(
                    self.phone_info.bluetooth_name))
        except Exception as e:
            logger.error("Trun on Bluetooth Button is not Visible")
            logger.error(repr(e))
        return is_start_discovery

    def bt_stop_discovery(self):
        """
        Stop  Bluetooth discovery on phone
        :param:None
        :return:
            is_stop_discovery (boolean) :True if discovery stopped,
            False otherwise
        :raise:None
        """
        is_stop_discovery = False
        try:
            is_bluetooth_off = self.bt_radio('off')
            if is_bluetooth_off:
                logger.debug("Bluetooth discovery Stoped {}".format(
                    self.phone_info.bluetooth_name))
                is_stop_discovery = True
            else:
                logger.debug("Bluetooth discovery completed {}".format(
                    self.phone_info.bluetooth_name))
                is_stop_discovery = False
        except Exception as e:
            logger.error("Turn OFF Bluetooth Button is not Visible")
            logger.error(repr(e))
        return is_stop_discovery

    def is_same_bluetooth_name(self, device_to_connect,
                               bluetooth_device_name_to_connect):
        name_of_bluetooth = device_to_connect.text.replace('\u200e', '').strip().lower()
        bluetooth_device_to_connect = bluetooth_device_name_to_connect.strip().lower()
        if (name_of_bluetooth == bluetooth_device_to_connect) \
                or (name_of_bluetooth == "hr-" + bluetooth_device_to_connect) or (
                    name_of_bluetooth == "le-"+bluetooth_device_to_connect):
            return True
        return False

    def bt_connect_and_check(self, bluetooth_device_name_to_connect):
        """
        Connect phone with given bt device and check weather successfully
        connected.
        :param:
            bluetooth_device_name_to_connect(str) : bluetooth device name
            that you want to connect
        :return:
            is_connect_and_check (boolean): True if bluetooth is connected,
            False otherwise
        :raise:None
        """
        is_bt_connect_and_check = False
        try:
            is_bt_already_connected = self.bt_is_connected_to(
                bluetooth_device_name_to_connect)

            if is_bt_already_connected:
                is_bt_connect_and_check = True
            else:
                self.bt_connect(bluetooth_device_name_to_connect)
                is_bt_connect_and_check = self.bt_is_connected_to(
                    bluetooth_device_name_to_connect)
        except Exception as e:
            logger.error("Need to turn on bluetooth and DUT devices")
            logger.error(repr(e))
        return is_bt_connect_and_check

    def _bt_swipe_and_connect(self):
        try:
            sleep(3)
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_contact_access_allow_button,
                                                 5)
        except Exception as e:
            logger.warning("ALLOW CONTACT ACCESS BUTTON IS NOT VISIBLE")
            return False
        else:
            try:
                self.find_element(self.driver.appium_driver,
                                  self.bluetooth_contact_access_allow_button,
                                  0).click()
                self.find_element(self.driver.appium_driver,
                                  self.bluetooth_pair_button,
                                  0).click()
            except Exception as e:
                logger.warning("Fail to click bluetooth pair button")
                return False
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_pair_button,
                                                 5)
        except Exception as e:
            logger.warning("ACCESS PHONE BOOK REQUEST BUTTON IS NOT VISIBLE")
            return True
        else:
            self.find_element(self.driver.appium_driver,
                              self.bluetooth_pair_button,
                              0).click()

            return True

    def _allow_contact_access_for_samsung_device(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            if 'SM' in self._get_android_phone_model():
                try:
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver,
                        'self.android_locators.BLUETOOTH_CONTACT_ACCESS_ALLOW_BUTTON_ByXPATH',
                        10)
                    self.find_element(self.driver.appium_driver,
                                      'self.android_locators.BLUETOOTH_CONTACT_ACCESS_ALLOW_BUTTON_ByXPATH',
                                      0).click()
                except Exception as e:
                    logger.warning("Contact Access button is not visible")
                    logger.warning(repr(e))

    def _bt_retry_to_connect(self, bluetooth_device_name_to_connect):
        try:
            logger.debug("Waited 10 seconds to make sure device list visible")
            sleep(10) #Make sure device name is visible in Bluetooth Available device list
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_pair_device,
                                                 15)
            new_element_list = self.find_elements(self.driver.appium_driver,
                                                  self.bluetooth_pair_device,
                                                  1)
            for index in range(len(new_element_list)):
                name_of_bluetooth = new_element_list[index].text
                # On my iPhone 6 (iOS 11.1.1), I'm seeing that the
                # `name_of_bluetooth` will randomly not be a string (which
                # breaks the next if-statement entirely). So adding a quick
                # work-around here.
                # I've also been testing this with an iPhone 7 Plus (iOS
                # 10.3.2), and a Nexus 6P (Android 6.0.1).
                if type(name_of_bluetooth) is not str:
                    logger.debug("Ignoring non-string element: {!r}".format(
                        name_of_bluetooth))
                    continue
                if self.is_same_bluetooth_name(new_element_list[index],
                                               bluetooth_device_name_to_connect):
                    new_element_list[index].click()
                    self._bt_swipe_and_connect()
                    logger.debug(
                        "Connecting to " + bluetooth_device_name_to_connect)
                    return True

        except Exception as e:
            self.take_screenshot(self.driver.appium_driver,
                                 '__retry_to_bt_connect')
            logger.warning(
                "Connection is not successfully with bluetooth device")
            logger.warning(repr(e))
        return False

    def __retry_to_bt_connect(self, bluetooth_device_name_to_connect):
        try:
            if '8.1' in self.phone_info.os_version or self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.bluetooth_pair_new_device_in_android_8_1_button,
                                                     10)
                self.find_element(self.driver.appium_driver,
                                  self.bluetooth_pair_new_device_in_android_8_1_button,
                                  2).click()
        except:
            logger.debug("pair new device option is not available")
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_pair_device,
                                                 10)
            new_element_list = self.find_elements(self.driver.appium_driver,
                                                  self.bluetooth_pair_device,
                                                  1)
            for index in range(len(new_element_list)):
                if self.is_same_bluetooth_name(new_element_list[index],
                                               bluetooth_device_name_to_connect):
                    new_element_list[index].click()
                    break
        except Exception as e:
            self.take_screenshot(self.driver.appium_driver,
                                 '__retry_to_bt_connect')
            logger.warning(
                "Connection is not successfully with bluetooth device after "
                "retry")
            logger.warning(repr(e))

    def connect_paired_device(self, bluetooth_device_name_to_connect):
        self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                             self.paired_device_list, 10)
        list_of_pair_element = self.find_elements(self.driver.appium_driver,
                                                  self.paired_device_list,
                                                  1)
        for index in range(len(list_of_pair_element)):
            if self.is_same_bluetooth_name(list_of_pair_element[index],
                                           bluetooth_device_name_to_connect):
                sleep(2)
                list_of_pair_element[index].click()
                self._bt_swipe_and_connect()
                return True

    def _go_to_bluetooth_device_list_screen(self):
        # if '8.1' in self.phone_info.os_version or \
        #         self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
        try:
            logger.info("Press refresh_button to make dut available")
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_pair_new_device_refresh_button,
                                                 10)
            # time.sleep(
            #     5)  # added sleep to make sure screen has changed and we
            #  are on discovered device list screen.
        except Exception as e:
            logger.debug("pair new device option is not available")
            logger.error(repr(e))

        else:
            self.find_element(self.driver.appium_driver,
                              self.bluetooth_pair_new_device_refresh_button,
                              2).click()
            time.sleep(5)

    def _wait_for_bluetooth_device_to_be_conneted(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            # In particular, Wait for the UI on Android 6.0.1 to indicate
            # we've given up trying to connect to the phone.
            # This fixes some weirdness I was seeing in BayWolf due to slow
            # pairing/connecting.
            # While that connection was slowly setting up, the script would
            # assume it had failed.
            #  After this, further attempts to connect to the DUT would
            # break with the ever-mysterious "incorrect PIN or passkey" popup.
            logger.info(
                "Waiting for the 'Pairing...' or 'Connecting...' summary "
                "text to show up.")
            try:
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.bluetooth_status_summary,
                                                     20)
                logger.info(
                    "Waiting for the 'Pairing...' or 'Connecting...' summary "
                    "text to go away.")
                self.wait_till_element_to_be_invisible(
                    self.driver.appium_driver, self.bluetooth_status_summary,
                    20)
                self.wait_for_google_assistant_pop_up_to_disappear()
            except:
                logger.info(
                    "Couldn't find the 'Pairing' or 'Connecting...' texts. "
                    "Assuming already connected.")
            time.sleep(1.0)  # Wait a little extra for things to settle.
        else:
            time.sleep(
                10)  # wait for 10 seconds  to make sure DUT is in Connected
            #  State
            logger.debug("Waited 10 seconds")
        self._allow_contact_access_for_samsung_device()

    def __is_available_device_screen(self):
        try:

            if self.phone_info.phone_type == PhoneType.ANDROID:
                sleep(10)  # requied time to change screen after successful BT Connection
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                  'self.android_locators.AVAILABLE_DEVICE_TEXT_ByXPATH', 0)
                return True
        except Exception as e:
            logger.warning(repr(e))
        return False

    def _select_bluetooth_device(self, bluetooth_device_name_to_connect,
                                 no_of_attempt):
        is_device_found = False
        check_dut_name = False
        try:
            logger.info("Unpair devices again if it still exists paired device")
            pair_list = self.bt_get_pairlist()
            if len(pair_list) > 0:
                for device in pair_list:
                    self.bt_unpair(device)

            self._go_to_bluetooth_device_list_screen()

            attempt_times = 0
            while True:
                attempt_times += 1
                logger.debug("Attempt times is %d: " % attempt_times)
                if attempt_times % 11 == 0:
                    logger.info("connection failed with {} bluetooth device".format(
                        bluetooth_device_name_to_connect))
                    return is_device_found

                if not is_device_found and attempt_times % 5 == 0:
                    self.bt_radio('off')
                    self.bt_radio('on')
                    time.sleep(10)

                try:
                    self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                         self.bluetooth_device_name_cancel_button, 2)
                except Exception as e:
                    pass
                else:
                    self.find_element(self.driver.appium_driver,
                                      self.bluetooth_device_name_cancel_button, 0).click()
                    logger.info("Return to the bluetooth Settings page")
                    time.sleep(1)

                logger.info("Get all available devices and then select dut device to test")
                try:
                    element_list = self.find_elements(self.driver.appium_driver,
                                                      self.bluetooth_pair_device_with_title, 0)

                except Exception as e:
                    continue

                device_list_length = len(element_list)
                if device_list_length < 4:
                    continue
                else:
                    for index in range(3, device_list_length):
                        logger.info(
                            "Select DUT device %s to begin preparing connection in available devices list" % bluetooth_device_name_to_connect)
                        try:
                            match_dut_name = self.is_same_bluetooth_name(element_list[index],
                                                                         bluetooth_device_name_to_connect)
                            if match_dut_name:
                                logger.debug("Found dut device")
                                check_dut_name = True
                                logger.info("Click DUT device to connect")
                                element_list[index].click()
                                time.sleep(2)
                                break
                            else:
                                logger.debug("Attempt to find dut device again")
                                time.sleep(0.1)

                        except Exception as e:
                            logger.error(
                                "Select next device to begin preparing connection in available devices list")
                            time.sleep(5)
                            break

                if not check_dut_name:
                    logger.debug("The dut device is not found, retry it.")
                    time.sleep(2)
                    continue

                logger.info("Connect to dut bluetooth device %s" % bluetooth_device_name_to_connect)
                if not self.check_if_bt_pairing_fail():
                    if self._bt_swipe_and_connect():
                        logger.debug("Connecting to " + bluetooth_device_name_to_connect)
                        time.sleep(5)
                        is_device_found = True
                        return is_device_found
                    else:
                        time.sleep(2)
                        continue
                else:
                    time.sleep(2)
                    continue
        except:
            logger.info("connection failed with {} bluetooth device".format(
                bluetooth_device_name_to_connect))
            raise
        return is_device_found

    def cancel_goggle_assistant_setup(self):
        try:
            self.driver.appium_driver.open_notifications()
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 'self.android_locators.BLUETOOTH_DONT_ASK_FOR_GA_SETUP_ByXPATH',
                                                 10)
            self.find_element(self.driver.appium_driver,
                              'self.android_locators.BLUETOOTH_DONT_ASK_FOR_GA_SETUP_ByXPATH',
                              0).click()
        except:
            self.driver.appium_driver.back()
            logger.warning("GA setup option not available")

    def _connect_bluetooth_device(self, bluetooth_device_name_to_connect,
                                  no_of_attempt, enable_ga):
        is_bt_paired = self.bt_is_paired_to(bluetooth_device_name_to_connect)
        if is_bt_paired:
            self.bt_unpair(bluetooth_device_name_to_connect)
            if self.phone_info.phone_type == PhoneType.IOS:
                self.bt_radio('off')
                self.bt_radio('on')

        self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                             self.bluetooth_pair_device,
                                             10)
        sleep(2)  # Static Sleep to make DUT available in DUT.
        element_list = self.find_elements(self.driver.appium_driver,
                                          self.bluetooth_pair_device, 1)
        for element in element_list:
            if bluetooth_device_name_to_connect in element.text:
                break
        else:
            self._go_to_bluetooth_device_list_screen()
            sleep(5)   # Make sure Device is available device list

        is_device_found = self._select_bluetooth_device(
            bluetooth_device_name_to_connect, no_of_attempt)
        if is_device_found and self.__is_available_device_screen():
            return True
            # is_device_found = self._bt_retry_to_connect(bluetooth_device_name_to_connect)
        elif is_device_found and not self.__is_available_device_screen():
            self._wait_for_bluetooth_device_to_be_conneted()
            if self.bt_is_connected():
                if enable_ga:
                    if self.phone_info.phone_type == PhoneType.ANDROID:
                        self.set_up_google_assistant()
                else:
                    self.cancel_goggle_assistant_setup()
                self._go_to_connected_device_screen(no_of_back_click=1)
                return True
        return False

    def bt_connect(self, bluetooth_device_name_to_connect, perform_unpair=True,
                   no_of_attempt=1, enable_ga=False):
        """
        Initiates a pair to a selected bluetooth device.
        To check if this pair succeeded, use is_paired().
        To check if any device is paired currently, use is_paired_with(mac)
        It is recommended to use pair_and_check(mac) instead.
        :param:
            bluetooth_device_name_to_connect (str) : Bluetooth device name
            that you want to connect
            perfrom_unpair(boolean) =True By Default it will Perform Unpiar
            DUT from Paired device list and then connect again.
                                     False - To avoide unpairing and connect
                                     DUT from paired device list
            no_of_attempt (Int)=Default value=4
            no of no_of_attempt is 4 to connect bluetooth device in case
            failure in first attempt
        :return:
            (boolean) = True if device connected.False otherwise
        :raise:
            None
        """
        try:
            is_already_connected = self.bt_is_connected_to(
                bluetooth_device_name_to_connect)
            if is_already_connected is True:
                return True

            if not perform_unpair:
                return self.connect_paired_device(
                    bluetooth_device_name_to_connect)

            return self._connect_bluetooth_device(
                bluetooth_device_name_to_connect, no_of_attempt, enable_ga)

        except Exception as e:
            self.take_screenshot(self.driver.appium_driver, 'bt_connect')
            if '8.1' in self.phone_info.os_version or self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
                self.driver.appium_driver.back()
            logger.error("Connection failed {} with bluetooth device".format(
                bluetooth_device_name_to_connect))
            logger.error(repr(e))
        return False

    def bt_try_connect(self, bluetooth_device_name_to_connect,
                       contact_sharing=False):  # TODO: Need to update to
        # use the new/refactored bt_connect() design from above.
        """
        The same as the bt_connect() function except that this will not try
        to wait to verify the connection via the phone.

        The idea here is we just fire off a connection attempt and wait for
        the DUT to confirm it's connected (via sink states).

        :param bluetooth_device_name_to_connect: Bluetooth device name that
        you want to connect
        :return: is_bluetooth_connect (boolean) = True if device
        paired.False otherwise
        :raise: None
        """
        is_bluetooth_connect = False
        try:
            is_already_connected = self.bt_is_connected_to(
                bluetooth_device_name_to_connect)
            if is_already_connected is True:
                is_bluetooth_connect = True
            else:
                is_bt_paired = self.bt_is_paired_to(
                    bluetooth_device_name_to_connect)
                if contact_sharing:
                    if is_bt_paired:
                        if self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
                            self.wait_till_element_to_be_visible(
                                self.driver.appium_driver,
                                self.previously_paired_device_button, 5)
                            self.find_element(self.driver.appium_driver,
                                              self.previously_paired_device_button,
                                              0).click()
                        self.wait_till_element_to_be_visible(
                            self.driver.appium_driver, self.paired_device_list,
                            10)
                        pair_element = self.find_elements(
                            self.driver.appium_driver, self.paired_device_list,
                            1)
                        for index in range(len(pair_element)):
                            if self.is_same_bluetooth_name(pair_element[index],
                                                           bluetooth_device_name_to_connect):
                                pair_element[index].click()
                                # self._bt_swipe_and_connect(pair_element,
                                # index) # Not sure if this is required for
                                # tests to work? I can get my Nexus6P (
                                # Android 6.0.1) and iPhone 7 Plus (iOS
                                # 10.3.2) to work without it... (So far)
                                is_bluetooth_connect = True
                                self._go_to_connected_device_screen(
                                    no_of_back_click=1)
                                return is_bluetooth_connect
                else:
                    if is_bt_paired:
                        self.bt_unpair(bluetooth_device_name_to_connect)
                        self.bt_radio('off')
                        self.bt_radio('on')

                try:
                    if '8.1' in self.phone_info.os_version or self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
                        self.wait_till_element_to_be_visible(
                            self.driver.appium_driver,
                            self.bluetooth_pair_new_device_in_android_8_1_button,
                            10)
                        self.find_element(self.driver.appium_driver,
                                          self.bluetooth_pair_new_device_in_android_8_1_button,
                                          2).click()
                        sleep(10)
                except:
                    logger.debug("Pair new device option is not available")
                is_device_found = False
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.bluetooth_pair_device,
                                                     5)
                element_list = self.find_elements(self.driver.appium_driver,
                                                  self.bluetooth_pair_device,
                                                  1)
                # Wait till bluetooth device found in list and click when it
                #  is visible in list
                for retry in range(1):
                    if retry == 0:
                        for index in range(len(element_list)):
                            element_text = element_list[index].text
                            # For some reason my iPhone 6 (iOS 11.1.1) is
                            # getting stuck here because one of the
                            # element's text is None.
                            # So adding bit to ignore that.
                            if type(element_text) is not str:
                                logger.warn(
                                    "Found pairing list element's text was "
                                    "None! Ignoring for now.")
                                continue
                            if self.is_same_bluetooth_name(element_list[index],
                                                           bluetooth_device_name_to_connect):
                                element_list[index].click()
                                # self._bt_swipe_and_connect(element_list,
                                # index) # Not sure if this is required for
                                # tests to work? I can get my Nexus6P (
                                # Android 6.0.1) and iPhone 7 Plus (iOS
                                # 10.3.2) to work without it... (So far)
                                logger.debug("Connecting to " +
                                             bluetooth_device_name_to_connect)
                                is_device_found = True
                                # NOTE: Removed a bunch of stuff after this...
                                break
                    else:
                        is_device_found = self._bt_retry_to_connect(
                            bluetooth_device_name_to_connect)
                    if is_device_found == False:
                        if '8.1' in self.phone_info.os_version \
                                or self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
                            self.driver.appium_driver.back()
                        self.bt_radio('off')
                        self.bt_radio('on')
                        self.perform_bottom_to_up_swipe(
                            self.driver.appium_driver)
                        logger.debug("Retries count : " + str(retry))
                        sleep(1)
                    else:
                        # The below can become strangely slow (take ~12
                        # seconds) randomly, so skipping it...
                        # is_bt_button_visible = self.__verify_current_screen()
                        # logger.debug("The BT button is visible? {
                        # }".format(is_bt_button_visible))
                        # if not is_bt_button_visible:
                        #    self.__retry_to_bt_connect(
                        # bluetooth_device_name_to_connect)
                        break
                if is_device_found:
                    is_bluetooth_connect = True
                else:
                    self.take_screenshot(self.driver.appium_driver,
                                         'bt_connect')
                    logger.error("Not connecting to given mobile Device")
        except Exception as e:
            if '8.1' in self.phone_info.os_version or \
                    self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
                self.driver.appium_driver.back()
            self.take_screenshot(self.driver.appium_driver, 'bt_connect')
            logger.error(
                "Connection is not successfully with bluetooth device")
            logger.error(repr(e))
        return is_bluetooth_connect

    def bt_is_connected_to(self, blutooth_connected_device_name):
        """
        Tests if phone is connected to a specific bluetooth device
        :param:
            blutooth_connected_device_name (str) : Name of device that need
            to verify is connected
        :return:
        (Boolean) = True, False (True = connected, False = disconnected)
        :raise:None
        """
        bt_is_connected = False
        logger.debug("Checking if Phone is connected to {!r}".format(
            blutooth_connected_device_name))
        try:
            logger.debug("Is the phone connected to something? {!r}".format(
                bt_is_connected))
            bt_is_connected = self.bt_is_connected()

            if bt_is_connected is False:
                return False
            # self.wait_for_google_assistant_pop_up_to_disappear(max_wait=20)
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_connected_device_list,
                                                 10)
            connected_device_list = self.find_elements(
                self.driver.appium_driver,
                self.bluetooth_connected_device_list, 1)
            if connected_device_list is not None:
                for index in range(len(connected_device_list)):
                    logger.debug(
                        "Checking if {!r} is the device in question"
                        " (i.e. {!r})".format(connected_device_list[index].text,
                                              blutooth_connected_device_name))
                    if self.is_same_bluetooth_name(connected_device_list[index],
                                                   blutooth_connected_device_name):
                        logger.debug("Is Bluetooth Connected with given device {}".format(
                                     blutooth_connected_device_name))
                        return True
        except Exception as e:
            logger.warning(
                "Need to attempt connect before bt_is_connected_to.")
            logger.warning(repr(e))
        return False

    def bt_is_not_connected_to(self, bluetooth_not_connected_device_name):
        """
        Tests if phone is  not connected to a specific bluetooth device
        :param:
            blutooth_connected_device_name (str) : Name of the device that
            need to verify is not connected
        :return:
            (boolean) : True, False (True = connected, False = disconnected)
        :raise:
            None
        """
        try:
            is_bt_connected_to_device = self.bt_is_connected_to(
                bluetooth_not_connected_device_name)
            if not is_bt_connected_to_device:
                logger.debug(
                    'Bluetooth is not connected with given device {}'.format(
                        bluetooth_not_connected_device_name))
                return True

            logger.debug('Bluetooth is connected with given device {}'.format(
                bluetooth_not_connected_device_name))
        except Exception as e:
            logger.warning(
                "Perform unpair/disconnect before performing "
                "bt_is_not_connected_to ")
            logger.warning(repr(e))
        return False

    def get_name(self):
        """
         get Buletooth Name of Mobile Device.
         :param:None
         :return:
             device_name(str): Bluetooth Name
         :raise:None
        """
        device_name = ''
        if self.phone_info.phone_type == PhoneType.IOS:
            is_general_visible = False
            try:
                try:
                    # verify that  General Button
                    self.find_element(self.driver.appium_driver,
                                      'self.ios_locators.GENERAL_NAVIGATION_BUTTON_ByXPATH',
                                      1).text
                    is_general_visible = True
                except:
                    logger.debug("General Button is currently not visible ")

                if is_general_visible:
                    pass
                else:
                    self.driver.appium_driver.close_app()
                    self.driver.appium_driver.launch_app()
                    logger.debug(
                        'STEP -: Navigate to general and about in settings  '
                        '- ')
                    self.find_element(self.driver.appium_driver,
                                      self.general_button_settings).click()
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver, self.status_button, 10)
                    self.find_element(self.driver.appium_driver,
                                      self.status_button).click()

                device_name = self.find_element(self.driver.appium_driver,
                                                self.device_name).text
                logger.debug("Bluetooth Device Name:{}".format(device_name))
            except Exception as e:
                logger.warning('Device name is not Visible')
                logger.debug(repr(e))
        elif self.phone_info.phone_type == PhoneType.ANDROID:
            name_text_box = False
            is_bluetooth_button__visible = self.__verify_current_screen()
            try:
                if not is_bluetooth_button__visible:
                    logger.debug(
                        'STEP -: Navigate to bluetooth screen in settings  - ')
                    # On my Nexus 6P + Android 8.0.0, found that wasn't
                    # going to the Bluetooth settings menu correctly,
                    # So using the below function instead. I think it's what
                    #  was intended, (but maybe didn't get
                    # switched in everywhere once it was created?).
                    self._go_to_bluetooth_button()

                bluetooth_element = self.find_element(
                    self.driver.appium_driver,
                    self.bluetooth_button_on_off_button)
                # if bluetooth is OFF then throw Exception
                if bluetooth_element.text is False or bluetooth_element.text == 'OFF':
                    bluetooth_element.click()
                    logger.debug("Bluetooth turned on in device with device_name " +
                        self.phone_info.bluetooth_name)
                else:
                    logger.debug("Bluetooth is already on " + self.phone_info.bluetooth_name)
                try:
                    self.find_element(self.driver.appium_driver,
                                      self.device_name_text_box, 1).is_displayed()
                    name_text_box = True
                except:
                    logger.debug("Device name text box is not visible")
                if name_text_box is True:
                    device_name = self.find_element(self.driver.appium_driver,
                                                    self.device_name_text_box).text
                else:

                    self.find_element(self.driver.appium_driver,
                                      self.bluetooth_more_options_button, 1).click()
                    self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                         self.device_name, 10)
                    self.find_element(self.driver.appium_driver, self.device_name).click()
                    self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                         self.device_name_text_box, 10)
                    device_name = self.find_element(self.driver.appium_driver,
                                                    self.device_name_text_box).text
                logger.debug("Bluetooth Device Name:" + device_name)
            except Exception as e:
                logger.warning('Bluetooth Device name is not Visible')
                logger.debug(repr(e))
        return device_name

    def set_name(self, set_device_name):
        """
        Set Buletooth Name of Mobile Device.
        :param:
            set_device_name (str) : Name of the bluetooth that you want to set
        :return:
            is_device_name_set (boolean): True if bluetooth name is
            set.False otherwise
        :raise:None
        """
        is_device_name_set = False
        if self.phone_info.phone_type == PhoneType.IOS:
            is_general_visible = False
            try:
                try:
                    # verify that  General Button
                    self.find_element(self.driver.appium_driver,
                                      'self.ios_locators.GENERAL_NAVIGATION_BUTTON_ByXPATH',
                                      1).is_displayed()
                    is_general_visible = True
                except:
                    logger.debug("General Button is currently not visible ")

                if is_general_visible:
                    pass
                else:
                    self.driver.appium_driver.close_app()
                    self.driver.appium_driver.launch_app()
                    logger.error('Navigate to general and about in settings')
                    self.find_element(self.driver.appium_driver,
                                      self.general_button_settings).click()
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver, self.status_button, 10)
                    self.find_element(self.driver.appium_driver,
                                      self.status_button).click()

                self.find_element(self.driver.appium_driver,
                                  self.device_name).click()
                text_field = self.find_element(self.driver.appium_driver,
                                               self.device_name_text_box).clear()

                self.driver.appium_driver.set_value(text_field,
                                                    set_device_name)
                self.find_element(self.driver.appium_driver,
                                  self.set_name_button).click()
                is_device_name_set = True

                logger.debug('Set New Name of Mobile Phone  - ',
                             set_device_name)
            except Exception as e:
                logger.warning("Bluetooth Device name is not Set")
                logger.debug(repr(e))
        elif self.phone_info.phone_type == PhoneType.ANDROID:
            name_text_box = False
            is_bluetooth_button__visible = self.__verify_current_screen()
            try:
                try:
                    self.find_element(self.driver.appium_driver,
                                      self.device_name_text_box,
                                      1).is_displayed()
                    name_text_box = True
                except:
                    logger.debug("Device name text box is not visible")
                if name_text_box is True:
                    device_name = self.find_element(self.driver.appium_driver,
                                                    self.device_name_text_box).clear()
                    self.driver.appium_driver.set_value(device_name,
                                                        set_device_name)
                    self.find_element(self.driver.appium_driver,
                                      self.set_name_button).click()
                    is_device_name_set = True
                    logger.debug(
                        ':Set New Name of Mobile Phone  - ' + set_device_name)
                elif name_text_box is False:
                    if is_bluetooth_button__visible:
                        pass
                    else:
                        self.testcase_action = 'STEP -: Go to Bluetooth ' \
                                               'option from settings - '
                        self._go_to_bluetooth_button()

                    bluetooth_element = self.find_element(
                        self.driver.appium_driver,
                        self.bluetooth_button_on_off_button, 1)
                    # if bluetooth is OFF then throw Exception
                    if bluetooth_element.text is False or \
                                    bluetooth_element.text == 'OFF':
                        bluetooth_element.click()
                        logger.debug(
                            "Bluetooth is turned on in device with name " +
                            self.phone_info.bluetooth_name)

                    else:
                        logger.debug(
                            "Bluetooth is already on " +
                            self.phone_info.bluetooth_name)
                    self.find_element(self.driver.appium_driver,
                                      self.bluetooth_more_options_button).click()
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver, self.device_name, 10)
                    self.find_element(self.driver.appium_driver,
                                      self.device_name).click()
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver, self.device_name_text_box,
                        10)
                    device_name = self.find_element(self.driver.appium_driver,
                                                    self.device_name_text_box).clear()
                    self.driver.appium_driver.set_value(device_name,
                                                        set_device_name)
                    self.find_element(self.driver.appium_driver,
                                      self.set_name_button).click()
                    is_device_name_set = True
                    logger.debug(
                        ':Set New Name of Mobile Phone  - ' + set_device_name)
            except Exception as e:
                logger.warning("Bluetooth Device name is not Set")
                logger.debug(repr(e))
        return is_device_name_set

    def get_mac(self):
        """
        Get bluetooth MAC addrress of Mobile Device.
        :param:None
        :return:
            bluetooth_mac_address (str): MAC address of bluetooth in mobile
            device
        :raise:None
        """
        bluetooth_mac_address = ''
        is_general_visible = False
        if self.phone_info.phone_type == PhoneType.IOS:
            try:
                try:
                    # verify that  General Button is visible
                    self.find_element(self.driver.appium_driver,
                                      'self.ios_locators.GENERAL_NAVIGATION_BUTTON_ByXPATH',
                                      0).is_displayed()
                    is_general_visible = True
                except:
                    logger.debug("General Button is currently not visible ")

                if is_general_visible:
                    pass
                else:

                    self.find_element(self.driver.appium_driver,
                                      self.general_button_settings).click()
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver, self.status_button, 10)
                    self.find_element(self.driver.appium_driver,
                                      self.status_button, 2).click()
                bluetooth_mac_address = self.find_element(
                    self.driver.appium_driver, self.bluetooth_mac_addess,
                    2).text
                logger.debug("Bluetooth Mac Address:" + bluetooth_mac_address)
            except Exception as e:
                logger.error("Bluetooth Mac Address is not Visible")
                logger.debug(repr(e))
        elif self.phone_info.phone_type == PhoneType.ANDROID:
            try:

                self.find_element(self.driver.appium_driver,
                                  self.general_button_settings).click()
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.status_button, 10)
                self.find_element(self.driver.appium_driver,
                                  self.status_button).click()

                self.testcase_action = 'STEP -: Get Bluetooth Mac Address'
                bluetooth_mac_address = self.find_element(
                    self.driver.appium_driver, self.bluetooth_mac_addess,
                    2).text
                logger.debug("Bluetooth Mac Address:" + bluetooth_mac_address)
            except Exception as e:
                logger.warning("Mac address is not available")
                logger.debug(repr(e))
        return bluetooth_mac_address

    def clearPhone(self, dut_name):
        """
          Clear Phone to unpair bluetooth device with mobile device and
          disable bluetooth.
          :param:
            dut_name (str) : DUT name to unpair
          :return:
            is_phone_clear(boolean) : True = phone clear , False = phone not
            clear
          :raise:None
        """
        is_phone_clear = True
        try:

            is_paired = self.bt_is_paired()
            if is_paired == False:
                is_phone_clear = True
            else:
                is_bt_disconnect = self.bt_disconnect(dut_name)
                is_bt_unpair = self.bt_unpair(dut_name)
                is_bt_off = self.bt_radio('off')
                self.bt_radio('on')
                if (is_bt_off) and (is_bt_unpair):
                    is_phone_clear = True
        except Exception as e:
            is_phone_clear = False
            logger.debug(repr(e))
        return is_phone_clear

    def kill_bluetooth_app(self):
        """
        kill Running appication
        :param:None
        :return:
            is_app_killed (boolean) : True = App killed , False = App not
            killed
        :raises:None
        """
        is_app_killed = False
        try:
            self.driver.appium_driver.quit()
            is_app_killed = True
        except Exception as e:
            logger.error(e)
        return is_app_killed

    def close_app(self):
        self.driver.appium_driver.close_app()

    def quit(self):
        """
        kill Running appication
        :param:None
        :return:
            is_app_killed (boolean) : True = App killed , False = App not
            killed
        :raises:None
        """
        is_app_quit = False
        try:
            self.driver.appium_driver.quit()
            is_app_quit = True
        except Exception as e:
            logger.error(e)
        return is_app_quit

    def set_airplane_mode(self, action):
        """
        Airplane Mode in mobile device
        :param:action(str):
        :return:
            is_action_performed (Boolean) :True Airplane Mode Activated,
            False Airplane Mode not Activated.
        :raises:None
        """

        is_action_performed = False
        is_airplane_mode_on_off_visible = False

        settings_more_button = \
            'self.android_locators.SETTINGS_MORE_BUTTON_ByXPATH'
        airplane_mode_on_off_toggle = \
            'self.android_locators.AIRPLANE_MODE_ON_OFF_ByID'

        if self.phone_info.phone_type == PhoneType.IOS:
            airplane_mode_on_off_toggle = \
                'self.ios_locators.AIRPLANE_MODE_ON_OFF_ByXPATH'
            no_sim_card_installed_msg = \
                'self.ios_locators.NO_SIM_CARD_INSTALLED_ByXPATH'
            no_sim_card_installed_ok_button = \
                'self.ios_locators.NO_SIM_CARD_INSTALLED_OK_BUTTON_ByXPATH'

        try:
            try:
                # verify that  Airplane Mode Button is visible
                is_airplane_mode_on_off_visible = self.find_element(
                    self.driver.appium_driver,
                    airplane_mode_on_off_toggle, 0).is_displayed()
            except:
                logger.debug(
                    "Airplane Mode ON/OFF button is currently not visible")

            if self.phone_info.phone_type == PhoneType.ANDROID:
                if not is_airplane_mode_on_off_visible:
                    self.driver.appium_driver.close_app()
                    self.driver.appium_driver.launch_app()
                    time.sleep(1)
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver, settings_more_button, 5)
                    self.find_element(self.driver.appium_driver,
                                      settings_more_button, 1).click()
                    # self.wait_till_element_to_be_visible(
                    # self.driver.appium_driver, airplane_mode_on_off_toggle)
                    logger.debug(
                        "Click on more button to make Airplane Mode visible")

                airplane_mode_toggle_status = self.find_element(
                    self.driver.appium_driver,
                    airplane_mode_on_off_toggle).text
                if airplane_mode_toggle_status.upper() == action.upper():
                    is_action_performed = True
                    logger.debug(
                        "Airplane Mode button set as {}".format(action))
                else:
                    self.find_element(self.driver.appium_driver,
                                      airplane_mode_on_off_toggle, 0).click()
                    is_action_performed = True
                    logger.debug(
                        "Airplane Mode button set as {}".format(action))
                self.driver.appium_driver.back()

            elif self.phone_info.phone_type == PhoneType.IOS:
                if not is_airplane_mode_on_off_visible:
                    self.driver.appium_driver.close_app()
                    self.driver.appium_driver.launch_app()
                    time.sleep(1)
                airplane_mode_toggle_status = self.find_element(
                    self.driver.appium_driver, airplane_mode_on_off_toggle,
                    0).text

                if action.upper() == "ON":
                    if (airplane_mode_toggle_status == False) or \
                            (airplane_mode_toggle_status == '1'):
                        is_action_performed = True
                        logger.debug(
                            "Airplane Mode button set as {}".format(action))
                        try:
                            self.wait_till_element_to_be_visible(
                                self.driver.appium_driver,
                                'self.ios_locators.OK_BUTTON_AFTER_BLUETOOTH_OFF_ByID',
                                3)
                            self.find_element(self.driver.appium_driver,
                                              'self.ios_locators.OK_BUTTON_AFTER_BLUETOOTH_OFF_ByID',
                                              0).click()
                        except:
                            pass

                    else:
                        self.find_element(self.driver.appium_driver,
                                          airplane_mode_on_off_toggle,
                                          0).click()
                        try:
                            self.wait_till_element_to_be_visible(
                                self.driver.appium_driver,
                                'self.ios_locators.OK_BUTTON_AFTER_BLUETOOTH_OFF_ByID',
                                3)
                            self.find_element(self.driver.appium_driver,
                                              'self.ios_locators.OK_BUTTON_AFTER_BLUETOOTH_OFF_ByID',
                                              0).click()
                        except:
                            pass
                        is_action_performed = True
                        logger.debug(
                            "Airplane Mode button set as {}".format(action))
                elif action.upper() == "OFF":
                    if (airplane_mode_toggle_status == True) or \
                            (airplane_mode_toggle_status == '0'):
                        is_action_performed = True
                        logger.debug(
                            "Airplane Mode button set as {}".format(action))
                    else:
                        self.find_element(self.driver.appium_driver,
                                          airplane_mode_on_off_toggle,
                                          0).click()
                        time.sleep(1)

                        is_action_performed = True
                        logger.debug(
                            "Airplane Mode button set as {}".format(action))
                else:
                    logger.debug(
                        "Only ON/OFF operation is possible with Airplane "
                        "Mode. {} option is not permitted".format(
                            action))

        except Exception as e:
            logger.error(
                "Exception occured while performing Airplane mode {} ".format(
                    action))
            logger.error(repr(e))

        return is_action_performed

    def _disconnect_bluetooth_device_from_ios_device(self):
        if self.phone_info.phone_type == PhoneType.IOS:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 'self.ios_locators.DISCONNECT_BUTTON_TO_DISCONNECT_BLUTOOTH_DEVICE_ByXPATH',
                                                 20)
            self.find_element(self.driver.appium_driver,
                              'self.ios_locators.DISCONNECT_BUTTON_TO_DISCONNECT_BLUTOOTH_DEVICE_ByXPATH',
                              0).click()
            time.sleep(1)
            self.find_element(self.driver.appium_driver,
                              'self.ios_locators.BLUETOOTH_SETTINGS_BACK_ByXPATH',
                              0).click()

    def bt_disconnect(self, device_name_to_disconnect):
        """
        Initiates a connection to a selected bluetooth device.
        To check if this pair succeeded, use is_connected().
        To check if any device is connected currently,
        use is_connected_with(mac)
        It is recommended to use connect_and_check(mac) instead.

        ex.  phone_obj.bluetooth.bt_disconnect(dut_obj.configProductName)
        :param:
            device_name_to_disconnect (str) : Bluetooth device name that you
            want to disconnect
        :return:
            is_bluetooth_disconnect (boolean) = True if device
            disconnect.False otherwise
        :raise:None
        """
        is_bluetooth_disconnect = False
        try:
            is_device_connected = self.bt_is_connected_to(
                device_name_to_disconnect)
            if is_device_connected is False:
                return True

            logger.debug('Disconnect Bluetooth device')
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_connected_device_list,
                                                 10)
            connected_device_list = self.find_elements(
                self.driver.appium_driver,
                self.bluetooth_connected_device_list,
                1)

            for index in range(len(connected_device_list)):
                if self.is_same_bluetooth_name(connected_device_list[index],
                                               device_name_to_disconnect):
                    if self.phone_info.phone_type == PhoneType.IOS \
                            or self.phone_info.os_version.startswith('9') or self.phone_info.os_version.startswith('10'):
                        # more_info = self.find_elements(
                        #     self.driver.appium_driver,
                        #     self.bluetooth_device_setting_button, 0)
                        # more_info[index].click()
                        connected_device_list[index].click()
                        break
                    else:
                        connected_device_list[index].click()
                        break

            self._disconnect_bluetooth_device_from_ios_device()
            if self.phone_info.phone_type == PhoneType.ANDROID:
                try:
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver,
                        'self.android_locators.BLUETOOTH_DISCONNECT_POP_UP_OK_BUTTON_ByXPATH',
                        10)
                    self.find_element(self.driver.appium_driver,
                                      'self.android_locators.BLUETOOTH_DISCONNECT_POP_UP_OK_BUTTON_ByXPATH',
                                      0).click()
                except:
                    logger.debug(
                        "Disconnect popup button is currently not available")

            is_bluetooth_disconnect = True

        except Exception as e:
            logger.warning("Need to attempt connect before disconnect")
            logger.warning(repr(e))
        self._go_to_connected_device_screen(no_of_back_click=1)
        return is_bluetooth_disconnect

    def enable_contact_sharing(self, dut_name, enable=False):
        """
        Enable/Disable Contact sharing on Mobile device
        ex. phone_obj.bluetooth.enable_contact_sharing('KLEOS',True)
        :param:
            dut_name (str) : Bluetooth device name
            enable (boolean) : True if you want to enable contact sharing
        :return:
            is_action_performed (boolean) = True if action performed.False
            otherwise
        :raise:None
        """
        try:
            self.wait_for_google_assistant_pop_up_to_disappear(20)
            is_device_connected = self.bt_is_connected_to(dut_name)
            if is_device_connected is False:
                logger.warning(
                    "Currently no bluetooth device is connected with"
                    " {}".format(self.phone_info.bluetooth_name))
                return False

            # self.bt_connect(dut_name)
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_connected_device_list,
                                                 10)
            connected_device_list = self.find_elements(
                self.driver.appium_driver,
                self.bluetooth_connected_device_list,
                1)

            for index in range(len(connected_device_list)):
                if self.is_same_bluetooth_name(connected_device_list[index],
                                               dut_name):
                    if (self.phone_info.os_version.startswith('11')) or (self.phone_info.os_version.startswith('8')) \
                            or (self.phone_info.os_version.startswith('9')) or self.phone_info.os_version.startswith('10'):
                        more_info = self.find_elements(
                            self.driver.appium_driver,
                            self.bluetooth_device_setting_button, 0)
                        more_info[index].click()
                    else:
                        self.find_element(self.driver.appium_driver,
                                          self.bluetooth_settings_button,
                                          1).click()
                    break
            if self.phone_info.phone_type == PhoneType.ANDROID:
                if '8.1' in self.phone_info.os_version or 'S8' in self.phone_info.bluetooth_name or \
                        (self.phone_info.os_version.startswith('9')) or (self.phone_info.os_version.startswith('10')):
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver,
                        self.contact_sharing_button_in_android_8_1_switch, 20)
                    contact_sharing_status = self.find_element(
                        self.driver.appium_driver,
                        self.contact_sharing_button_in_android_8_1_switch,
                        0)
                else:
                    self.wait_till_element_to_be_visible(
                        self.driver.appium_driver,
                        self.contact_sharing_checkbox, 20)
                    contact_sharing_status = self.find_element(
                        self.driver.appium_driver,
                        self.contact_sharing_checkbox, 0).\
                        get_attribute("checked")

                    # Now click that button if we're in the wrong state.

                switch_is_on = self.is_switch_on(contact_sharing_status)
                if enable != switch_is_on:
                    logger.debug(
                        "For phone {!r}, found that Switch is currently {}."
                        "Toggling so will be {}.".format(
                            self.phone_info.bluetooth_name,
                            "Enable" if switch_is_on else "Disable",
                            "Enable" if enable else "Disable",
                        ))
                    self.find_element(self.driver.appium_driver,
                                      self.contact_sharing_button, 0).click()
                    self.driver.appium_driver.back()
                    self.bt_disconnect(dut_name)
                    self._go_to_connected_device_screen(1)
                    self.bt_connect(dut_name, perform_unpair=False)

                else:
                    logger.debug(
                        "For phone {!r}, found that Switch is already {}."
                        "Leaving it that way.".format(
                            self.phone_info.bluetooth_name,
                            "ON" if switch_is_on else "OFF",
                        ))

                return True
        except Exception as e:
            logger.warning(
                "Could not enable/disable contact sharing on connected "
                "mobile devices {}"
                .format(self.phone_info.bluetooth_name))
            logger.warning(repr(e))
        return False

    def _go_to_audio_call_routing_option(self):
        self.driver.appium_driver.close_app()
        self.driver.appium_driver.launch_app()
        logger.debug(
            'Navigate to Settings -> General -> Accessibility -> Call Audio '
            'Routing')
        self.driver.appium_driver.execute_script("mobile: swipe",
                                                 {"direction": "up"})
        general_button = self.find_element(self.driver.appium_driver,
                                           self.general_button_settings, 2)
        general_button.click()
        logger.debug("Clicked on General button")
        # On my iPhone 7 Plus (iOS 10.3.2) this click() needs to be run twice...
        if self.phone_info.os_version.startswith('10') and self.phone_info.phone_type is PhoneType.IOS:
            logger.debug("Clicking the button again. (On iOS 10 the first click doesn't register.)")
            general_button.click()
        sleep(7) #Added Static sleep as is_display=False for iOS 12.wait_till_element visible will not work.
        self.find_element(self.driver.appium_driver,
                          'self.ios_locators.ACCESSIBILITY_BUTTON_ByXPATH'
                          '').click()
        logger.debug("Clicked on Accessibility button")
        self.driver.appium_driver.execute_script("mobile: scroll",
                                                 {"direction": "down"})

    def _is_audio_call_routing_option_availalble(self):
        try:
            self.find_element(self.driver.appium_driver,
                              'self.ios_locators.CALL_AUDIO_ROUTING_BUTTON_ByXPATH',
                              1).is_displayed()
            return True
        except Exception as e:
            logger.warning("Audio Call Routing Screen is not visible")
            logger.warning(repr(e))

    def get_audio_call_routing_status(self):
        if not self._is_audio_call_routing_option_availalble():
            self._go_to_audio_call_routing_option()
        call_audio_routing_status = self.find_element(
            self.driver.appium_driver,
            'self.ios_locators.CALL_AUDIO_ROUTING_STATUS_ByXPATH').text
        logger.debug("selected audio call routing option is {}".format(
            call_audio_routing_status))
        self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                             'self.ios_locators.GENERAL_BUTTON_ByID',
                                             5)
        self.find_element(self.driver.appium_driver,
                          'self.ios_locators.GENERAL_BUTTON_ByID').click()
        self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                             'self.ios_locators.SETTING_BUTTON_ByID',
                                             5)
        self.find_element(self.driver.appium_driver,
                          'self.ios_locators.SETTING_BUTTON_ByID', 0).click()
        self.driver.appium_driver.execute_script("mobile: scroll",
                                                 {"direction": "up"})
        return call_audio_routing_status

    def select_call_audio_routing(self, target_type):
        """
        Set Call Routing option on iOS Mobile device
        ex.  phone_obj.bluetooth.select_call_audio_routing('automatic')
        :param:
            target_type = automatic OR bluetooth headset OR speaker
        :return:
            is_action_performed (boolean) = True if action performed.False
            otherwise
        :raise:None
        """
        is_action_performed = False
        try:
            call_audio_routing_status = self.get_audio_call_routing_status()
            if target_type.lower() not in call_audio_routing_status.lower():
                if not self._is_audio_call_routing_option_availalble():
                    self._go_to_audio_call_routing_option()
                self.find_element(self.driver.appium_driver,
                                  'self.ios_locators.CALL_AUDIO_ROUTING_BUTTON_ByXPATH').click()
                logger.debug("Clicked on Call Audio Routing button")
                call_routing_options_list = self.find_elements(
                    self.driver.appium_driver,
                    'self.ios_locators.OPTION_CALL_ROUTING_BUTTON_ByXPATH')
                for call_routing_option in call_routing_options_list:
                    if target_type.lower() in call_routing_option.text.lower():
                        call_routing_option.click()
                        logger.debug(
                            "Audio Call Routing Option {} is Selected ".format(
                                target_type))
                        is_action_performed = True
                        self.find_element(self.driver.appium_driver,
                                          'self.ios_locators.ACCESSIBILITY_BUTTON_ByID',
                                          0).click()
                        break
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 'self.ios_locators.GENERAL_BUTTON_ByID',
                                                 5)
            self.find_element(self.driver.appium_driver,
                              'self.ios_locators.GENERAL_BUTTON_ByID').click()
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 'self.ios_locators.SETTING_BUTTON_ByID',
                                                 5)
            self.find_element(self.driver.appium_driver,
                              'self.ios_locators.SETTING_BUTTON_ByID',
                              0).click()
        except Exception as e:
            logger.error(
                "Exception occurred while setting call routing mode {} "
                "".format(
                    target_type))
            logger.error(repr(e))
        return is_action_performed

    def is_next_button_google_assistant_screen(self):
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 'self.android_locators.BLUETOOH_NEXT_BUTTON_GOOGLE_ASSISTANT_ByXPATH',
                                                 5)
            self.find_element(self.driver.appium_driver,
                              'self.android_locators.BLUETOOH_NEXT_BUTTON_GOOGLE_ASSISTANT_ByXPATH',
                              0)
            return True
        except:
            logger.debug("Google Assistant SetUp Option is not Available")
        return False

    def is_google_assistant_set_up_available(self):
        is_google_assiatant_setup_button_visible = False
        try:
            self.driver.appium_driver.open_notifications()
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 'self.android_locators.BLUETOOTH_FINISH_GOOGLE_ASSISTANT_SETUP_ByXPATH',
                                                 5)
            is_google_assiatant_setup_button_visible = self.find_element(
                self.driver.appium_driver,
                'self.android_locators.BLUETOOTH_FINISH_GOOGLE_ASSISTANT_SETUP_ByXPATH',
                0).is_displayed()
        except:
            logger.debug("Google Assistant SetUp Option is not Available")
            self.driver.appium_driver.back()
        return is_google_assiatant_setup_button_visible

    def _click_continue_to_setup_google_assistant(self):
        """
           Click on continue screen if it appears during GA Setup.
        """
        try:
            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 'self.android_locators.BLUETOOTH_CONTINUE_BUTTON_ByID',
                                                 10)
            self.find_element(self.driver.appium_driver,
                              'self.android_locators.BLUETOOTH_CONTINUE_BUTTON_ByID',
                              0).click()
        except Exception as e:
            logger.error(repr(e))
            logger.debug(
                "Continue setup screen is not available on Connected {} Mobile Device.Exception Message {}".format(
                    self.phone_info.bluetooth_name, e))

    def set_up_google_assistant(self):
        try:
            is_google_assiatant_setup_button_visible = self.is_google_assistant_set_up_available()
            if is_google_assiatant_setup_button_visible:
                self.find_element(self.driver.appium_driver,
                                  'self.android_locators.BLUETOOTH_FINISH_GOOGLE_ASSISTANT_SETUP_ByXPATH',
                                  0).click()
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     'self.android_locators.BLUETOOH_NEXT_BUTTON_GOOGLE_ASSISTANT_ByXPATH',
                                                     20)
                self.find_element(self.driver.appium_driver,
                                  'self.android_locators.BLUETOOH_NEXT_BUTTON_GOOGLE_ASSISTANT_ByXPATH',
                                  0).click()
                self._click_continue_to_setup_google_assistant()
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     'self.android_locators.BLUETOOTH_DONE_BUTTON_GOOGLE_ASSISTANT_ByXPATH',
                                                     60)
                self.find_element(self.driver.appium_driver,
                                  'self.android_locators.BLUETOOTH_DONE_BUTTON_GOOGLE_ASSISTANT_ByXPATH',
                                  0).click()
                logger.debug(
                    "Set up of Google Assistant is Completed on Connected {} Mobile Device.".format(
                        self.phone_info.bluetooth_name))
                self.driver.appium_driver.back()
                return True
            logger.debug(
                "Google Assistant SetUp Option is not Available on Connected {}.".format(
                    self.phone_info.bluetooth_name))
            return False
        except Exception as e:
            logger.error(repr(e))

    def _toggle_switch(self, element_for_toggle, enable):
        try:
            if element_for_toggle.get_attribute("checked"):
                if element_for_toggle.get_attribute("checked").lower() == "false":
                    switch_is_on = False
                if element_for_toggle.get_attribute("checked").lower() == "true":
                    switch_is_on = True
            else:
                switch_is_on = self.is_switch_on(element_for_toggle)

            if enable != switch_is_on:
                logger.debug(
                    "For phone {!r}, found that Switch is currently {}.Toggling so will be {}.".format(
                        self.phone_info.bluetooth_name,
                        "Enable" if switch_is_on else "Disable",
                        "Enable" if enable else "Disable",
                    ))
                element_for_toggle.click()
            else:
                logger.debug(
                    "For phone {!r}, found that Switch is already {}.Leaving it that way.".format(
                        self.phone_info.bluetooth_name,
                        "ON" if switch_is_on else "OFF",
                    ))
            return True
        except Exception as e:
            logger.warning("Could not Toggle Switch on mobile devices")
            logger.warning(repr(e))
            return False

    def enable_disable_media_sharing(self, dut_name, enable=True):

        """
        Enable/Disable Media sharing on Mobile device
        ex. phone_obj.bluetooth.enable_disable_media_sharing('KLEOS',True)
        :param:
            dut_name (str) : Bluetooth device name
            enable (boolean) : True if you want to enable media sharing
        :return:
            is_media_sharing_action_performed (boolean) = True if action performed.False otherwise
        :raise:None

        """
        try:
            is_bluetooth_button__visible = self.__verify_current_screen()
            if not is_bluetooth_button__visible:
                self._go_to_bluetooth_button()

            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.bluetooth_connected_device_list,
                                                 20)
            device_name = self.find_elements(self.driver.appium_driver,
                                             self.bluetooth_connected_device_list,
                                             0)

            for index in range(len(device_name)):
                if self.is_same_bluetooth_name(device_name[index], dut_name):
                    if (self.phone_info.os_version.startswith('11')) or (self.phone_info.os_version.startswith('8')):
                        more_info = self.find_elements(
                            self.driver.appium_driver,
                            self.bluetooth_device_setting_button, 0)
                        more_info[index].click()
                    else:
                        self.find_element(self.driver.appium_driver,
                                          self.bluetooth_settings_button,
                                          1).click()
                    break

            self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                 self.media_sharing_switch, 10)
            media_sharing_element = self.find_element(
                self.driver.appium_driver, self.media_sharing_switch, 0)

            # Now click that button if we're in the wrong state.
            is_media_sharing_action_performed = self._toggle_switch(
                media_sharing_element, enable)
            logger.debug(
                "Media Sharing option is set to {} on connected bluetooth devices {}".format(
                    enable, dut_name))
            return is_media_sharing_action_performed
        except Exception as e:
            logger.warning(
                "Could not enable/disable media sharing on connected mobile devices"
                .format(self.phone_info.bluetooth_name))
            logger.warning(repr(e))
            return False

    def set_media_volume_sync(self, dut_name, enable=True):
        """
        Enable/Disable Media Sync Volume on Mobile device
        ex. phone_obj.bluetooth.set_media_volume_sync(enable=True)
        :param:
            enable (boolean) : True if you want to enable Media Volume sync
        :return:
          is_media_volume_sync = True(boolean) if action performed.False otherwise
        :raise:None

        """
        try:
            if self.phone_info.phone_type == PhoneType.ANDROID and 'SM' in self._get_android_phone_model():
                is_bt_connected_to_device = self.bt_is_connected_to(dut_name)
                if not is_bt_connected_to_device:
                    logger.debug(
                        'For phone found that DUT {} is not connected with {} , '
                        'So Media Volume Sync option is not available '.format(
                            dut_name,
                            self.phone_info.bluetooth_name))
                    return False

                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.bluetooth_more_options,
                                                     5)
                self.find_element(self.driver.appium_driver,
                                  self.bluetooth_more_options, 0).click()

                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.media_volume_text,
                                                     10)
                self.find_element(self.driver.appium_driver,
                                  self.media_volume_text, 0).click()

                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     self.media_volume_sync_switch,
                                                     10)

                volume_sync_switch = self.find_element(
                    self.driver.appium_driver, self.media_volume_sync_switch,
                    0)

                # Now click that button if we're in the wrong state.
                is_media_volume_sync = self._toggle_switch(volume_sync_switch,
                                                           enable)
                self.driver.appium_driver.back()
                logger.debug(
                    "Media Volume option is set to {} on connected bluetooth devices {}".format(
                        enable, dut_name))
                return is_media_volume_sync
            logger.warning(
                "Media Volume Sync Option is not available on {} connected bluetooth devices".format(
                    self.phone_info.bluetooth_name))
        except Exception as e:
            logger.warning(
                "Could not enable/disable Media Volume Sync on connected mobile devices {}"
                .format(self.phone_info.bluetooth_name))
            logger.warning(repr(e))
            return False

    def wait_for_google_assistant_pop_up_to_disappear(self, max_wait=30):
        """
        Waits for the google assistant popup to go away.
        This is useful as on my Nexus 6P with Android 8.0.0, this popup often obscures the Bluetooth button. Attempts to press that button cause the phone to enter the Google assistant setup flow, which breaks the test.
        :param max_wait: The max number of seconds to wait for the popup to disappear. Default is 15. This value isn't exact.
        """
        if self.phone_info.phone_type == PhoneType.ANDROID:
            if self.is_next_button_google_assistant_screen():
                self.driver.appium_driver.back()
                self.wait_till_element_to_be_visible(self.driver.appium_driver,
                                                     'self.android_locators.BLUETOOTH_EXIT_GA_SETUP_BUTTON_ByXPATH',
                                                     10)
                self.find_element(self.driver.appium_driver,
                                  'self.android_locators.BLUETOOTH_EXIT_GA_SETUP_BUTTON_ByXPATH',
                                  0).click()
            logger.debug(
                "Starting wait for the 'Setup Google Assistant' pop up.")
            for _ in range(max_wait):
                logger.debug(
                    "Starting search for the 'Setup Google Assistant' pop up.")
                popup = self.find_element(
                    self.driver.appium_driver,
                    'self.android_locators.BLUETOOTH_FINISH_GOOGLE_ASSISTANT_'
                    'SETUP_ByXPATH', 0,
                    # Must be 0. If set to 1 or more, can cause this call to
                    # wait over 10 seconds. (Not sure if that's intentional?)
                )
                logger.debug(
                    "Completed search for the 'Setup Google Assistant' pop up.")
                if popup is not None:
                    logger.debug("Found the 'Setup Google Assistant' pop up.")
                else:
                    break
                time.sleep(1.0)

    def clear_all_notification(self, udid):
        try:
            if self.phone_info.phone_type == PhoneType.ANDROID:
                subprocess.Popen(f"adb -s {udid} shell input swipe 0 0 0 300", shell=True)
                sleep(2)
                clear_notification_button = self.find_element(self.driver.appium_driver, 'self.android_locators.CLEAR_NOTIFICATION_ByXPATH', 5)
                if clear_notification_button:
                    clear_notification_button.click()
                else:
                    logger.warning(f"Failed to clear notification on android devices {self.phone_info.bluetooth_name}")
                    return True
                logger.info(
                    f"All notifications has been cleared on android device: "
                    f"{self.phone_info.bluetooth_name}")
        except Exception as e:
            logger.warning(f"Failed to clear notification on android devices {self.phone_info.bluetooth_name}")
            self.driver.appium_driver.back()

    def terminate_app(self):
        self.driver.appium_driver.terminate_app(self.package_name)
