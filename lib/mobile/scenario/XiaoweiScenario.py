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
from wham_automation.utils.ConfigParser import get_appium_server_ip, get_android_madrid_app_package, \
    get_android_madrid_app_activity, get_madrid_login_user_name, get_madrid_login_user_password
from wham_automation.lib.mobile.scenario.BasePage import BasePage
from wham_automation.script_support.ScriptHelper import wait
from wham_automation.lib.framework.Configs.FrameworkConstants import PhoneType
from wham_automation.utils.log import logger
from wham_automation.test_scripts.Bamboo.lib.mobile.constants import HUAWEIConstant, XIAOMIConstant, OPPOConstant, VIVOConstant

MAX_DUT_TO_SEARCH_IN_CAROUSEL = 60

class XiaoweiScenario(BasePage):
    pre_check_result = False

    def __initialize_variable_of_xiaowei_app(self):
        """
        Initialize all variable used in Madrid application
        """
        if self.phone_info.phone_type == PhoneType.ANDROID:
            self.package_name = 'com.tencent.xw'
            self.activity_name = 'com.tencent.xw.ui.activitys.SplashActivity'
            self.xiaowei_main_page_activity_name = 'com.tencent.xw.ui.activitys.MainActivity'
            self.connection_prompt_xpath = '//android.widget.RelativeLayout'
            self.accept_button_xpath = '//android.widget.TextView[@resource-id="com.tencent.xw:id/ble_confirm_ensure"]'
            self.cancel_button_xpath = '//android.widget.TextView[@resource-id="com.tencent.xw:id/ble_confirm_cancel"]'
            self.device_icon_xpath = '//android.widget.RelativeLayout[@resource-id="com.tencent.xw:id/current_ble_headset"]'
            self.disconnect_button_xpath = '//android.widget.FrameLayout[@index="5"]/android.view.ViewGroup[@index="0"]/android.view.ViewGroup[@index="0"]'
            self.wechat_login_xpath = '//android.widget.TextView[@resource-id="com.tencent.xw:id/login_btn"]'
            self.agree_policy_xpath = '//android.widget.TextView[@resource-id="com.tencent.xw:id/agree_btn"]'
            self.device_name_xpath = '//android.widget.TextView[@resource-id="com.tencent.xw:id/headset_name"]'
            self.get_query_response_text = '//android.widget.LinearLayout[@resource-id="com.tencent.xw:id/feed_list_layout"]/descendant-or-self::android.widget.TextView'
            self.go_to_media_page_xpath = '//android.widget.ImageView[@resource-id="com.tencent.xw:id/left"]'
            self.get_media_name_xpath = '//android.widget.TextView[@resource-id="com.tencent.xw:id/music_name"]'
            self.go_to_home_page_xpath = '//android.widget.ImageView[@resource-id="com.tencent.xw:id/music_back_arrow"]'
            self.device_page_xpath = '//android.widget.TextView[@text="设备信息"]'
            brand_scenario_dict = {'HUAWEI': HUAWEIConstant,
                                    'XIAOMI': XIAOMIConstant,
                                     'OPPO' :OPPOConstant,
                                    'VIVO': VIVOConstant,
                                   }
            self.location_permission_xpath = brand_scenario_dict[self.phone_info.brand].location_permission_allow_always_ByXPATH
            self.phone_permission_xpath = brand_scenario_dict[self.phone_info.brand].phone_permission_allow_ByXPATH
            self.storage_permission_xpath = brand_scenario_dict[self.phone_info.brand].storage_permission_allow_ByXPATH
            self.record_permission_xpath = brand_scenario_dict[self.phone_info.brand].record_permission_allow_ByXPATH
            self.permission_allow_xpath = brand_scenario_dict[self.phone_info.brand].permission_allow_ByXPATH
            # *** added by Xinyu *** start
            self.tab_xiaowei_bg_xpath = '//android.widget.RelativeLayout[@resource-id="com.tencent.xw:id/tab_xiaowei_bg"]'
            self.btn_allow_always_xpath = brand_scenario_dict[self.phone_info.brand].ALLOW_ALWAYS_XPATH
            self.btn_allow_while_in_use_xpath = brand_scenario_dict[self.phone_info.brand].ALLOW_WHILE_IN_USE_XPATH
            self.btn_allow_xpath = brand_scenario_dict[self.phone_info.brand].ALLOW_XPATH
            self.btn_record_path = '//android.widget.TextView[@resource-id="com.tencent.xw:id/record_btn"'
            # *** added by Xinyu *** end

            # # wifi package and activity
            # self.wifi_package_name = brand_scenario_dict[self.phone_info.brand].wifi_settings_app_package
            # self.wifi_activity_name = brand_scenario_dict[self.phone_info.brand].wifi_app_activity
            #
            # # mobile network package and activity
            # self.mobile_network_package_name = brand_scenario_dict[self.phone_info.brand].mobile_network_settings_app_package
            # self.mobile_network_name = brand_scenario_dict[self.phone_info.brand].mobile_network_activity

        if self.phone_info.phone_type == PhoneType.IOS:
            self.package_name = 'com.tencent.xw'
            self.activity_name = 'com.tencent.xw'
            self.connection_prompt_xpath = '//XCUIElementTypeStaticText[@name="确认连接"]'
            self.accept_button_xpath = '//XCUIElementTypeButton[@name="连接"]'
            self.cancel_button_xpath = '//XCUIElementTypeButton[@name="取消"]'
            self.device_icon_xpath = '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' + \
            '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' + \
            '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeOther[2]/XCUIElementTypeImage[1]'
            self.disconnect_button_xpath = '//XCUIElementTypeStaticText[@name="断开连接"]'
            self.device_page_xpath = '//XCUIElementTypeStaticText[@name="设备信息"]'
            self.device_name_xpath = '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' + \
            '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' + \
            '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeOther[2]/XCUIElementTypeImage[1]/XCUIElementTypeStaticText[1]'
            self.get_query_response_text = '//XCUIElementTypeCell/XCUIElementTypeButton'
            self.get_query_text = '//XCUIElementTypeCell/XCUIElementTypeButton'
            self.get_response_text = '//XCUIElementTypeCell/XCUIElementTypeStaticText'
            self.key1 = '//XCUIElementTypeKey[@name="1"]'
            self.key2 = '//XCUIElementTypeKey[@name="2"]'
            self.key3 = '//XCUIElementTypeKey[@name="3"]'
            self.key4 = '//XCUIElementTypeKey[@name="4"]'
            self.key5 = '//XCUIElementTypeKey[@name="5"]'
            self.key6 = '//XCUIElementTypeKey[@name="6"]'
            self.key7 = '//XCUIElementTypeKey[@name="7"]'
            self.key8 = '//XCUIElementTypeKey[@name="8"]'
            self.key9 = '//XCUIElementTypeKey[@name="9"]'
            self.key0 = '//XCUIElementTypeKey[@name="0"]'

            # *** added by Xinyu *** start
            self.btn_record_path = '//XCUIElementTypeStaticText[@name="按 住 说 话"]'
            self.wechat_login_xpath = "//XCUIElementTypeButton[@name='微信登录']"
            self.agree_policy_xpath = "//XCUIElementTypeStaticText[@name='我已阅读，并同意']"
            self.btn_OK_xpath = "//XCUIElementTypeButton[@name='OK']"
            self.btn_allow_while_in_use_xpath = "//XCUIElementTypeButton[@name='Allow While Using App']"
            self.btn_allow_xpath = "//XCUIElementTypeButton[@name='Allow']"
            self.window_alert_xpath = "//XCUIElementTypeAlert"
            # *** added by Xinyu *** end

    def launch_xiaowei_app(self, driver=None):
        """
        Launch Xiaowei application
        :param:None
        :return:None
        :raises:None
        """
        #xiaowei will prmopt "check if connect to another device" window if open xiaowei after a xiaowei behavior. And 0.5s sleep.
        time.sleep(0.5)
        try:
            self.__initialize_variable_of_xiaowei_app()
            if driver:
                self.driver = driver
            else:
                self.driver = self.mobile_driver_factory_object.get_driver(get_appium_server_ip(),
                                                                           self.phone_info.appium_port,
                                                                           self.phone_info.platform_name,
                                                                           self.phone_info.os_version,
                                                                           self.phone_info.config_name,
                                                                           self.phone_info.uuid,
                                                                           self.package_name,
                                                                           self.activity_name,
                                                                           self.phone_info.wda_local_port)
        except Exception as e:
            logger.error(f'Driver launch  Fail on {self.phone_info.bluetooth_name}')
            logger.error(repr(e))
            return False
        else:
            return True

    def _verify_and_click_element(self, element, wait_time=5):
        """
        this is a common function used for verifying and clicking an element
        :param element: element by xpath
        :param wait_time: wait time and interval is 1s
        :return:
        """
        try:
            WebDriverWait(self.driver.appium_driver, wait_time, 1).until(lambda x: x.find_element_by_xpath(element))
        except Exception as e:
            logger.error(e)
            return False
        else:
            try:
                self.driver.appium_driver.find_element_by_xpath(element).click()
            except Exception as e:
                logger.error(e)
                return False
            else:
                return True

    def verify_connection_prompt(self, wait_time=5):
        """
        check the connection prompt
        :return: True
        """
        logger.info('Verify connection prompt')
        try:
            WebDriverWait(self.driver.appium_driver, wait_time, 1).until(lambda x: x.find_element_by_xpath(self.connection_prompt_xpath))
            return True
        except Exception as e:
            logger.error(e)
            logger.info('There is no xiaowei prompt in current page')
            return False

    def accept_connection_prompt(self, wait_time=5):
        """
        Tap accept button
        :return: True
        """
        logger.info('Accept connection prompt')
        try:
            WebDriverWait(self.driver.appium_driver, wait_time, 1).until(lambda x: x.find_element_by_xpath(self.accept_button_xpath))
            self.driver.appium_driver.find_element_by_xpath(self.accept_button_xpath).click()
            return True
        except Exception as e:
            logger.error(e)
            logger.info('There is no accept button')
            return False

    def cancel_connection_prompt(self, wait_time=5):
        """
        Tap cancel button
        :return: True
        """
        logger.info('Cancel connection prompt')
        try:
            WebDriverWait(self.driver.appium_driver, wait_time, 1).until(lambda x: x.find_element_by_xpath(self.cancel_button_xpath))
            self.driver.appium_driver.find_element_by_xpath(self.cancel_button_xpath).click()
            return True
        except Exception as e:
            logger.error(e)
            logger.info('There is no cancel button')
            return False

    def verify_device_icon(self, wait_time=5):
        """
        verify if device icon display, used fro verifying xiaowei connection
        :return: True
        """
        logger.info('Verify device icon')
        for i in range(wait_time):
            try:
                time.sleep(1)
                if self.driver.appium_driver.find_element_by_xpath(self.device_icon_xpath).is_displayed():
                    return True
            except Exception:
                pass
        else:
            logger.info('There is no device icon in current page')
            return False

    def insure_device_connection(self, wait_time=5):
        if not self.verify_device_icon(wait_time):
            result1 = self.verify_connection_prompt(wait_time)
            result2 = self.accept_connection_prompt()
            return (result1 and result2)
        else:
            logger.info('device is already connected')
            return True

    def go_to_device_page(self):
        logger.info('go to device page')
        self._verify_and_click_element(self.device_icon_xpath)
        try:
            result = self.driver.appium_driver.find_element_by_xpath(self.device_page_xpath)
            if result:
                logger.info('Go to device page successfully')
            else:
                logger.info('Fail to go to device page')
            return result
        except Exception as e:
            logger.error(e)
            logger.info('Fail to go to device page')
            return False

    def disconnect_device(self, count=5):
        for i in range(count):
            self.swip_down()
            device_status = self.go_to_device_page()
            if device_status:
                self.swip_up()
                time.sleep(1)
                result1 = self._verify_and_click_element(self.disconnect_button_xpath)
                if result1:
                    result2 = self.verify_device_icon(1)
                    if not result2:
                        logger.info('disconnect device successfully')
                        return True
        else:
            logger.info('Fail to disconnect device')
            return False

    def go_to_media_page(self):
        logger.info('go to media page')
        result = self._verify_and_click_element(self.go_to_media_page_xpath)
        if result:
            logger.info('Go to media streaming page successfully')
        else:
            logger.info('Fail to go to media streaming page')
        return result

    def get_current_media_name(self, wait_time=5):
        logger.info('get current media name')
        for i in range(wait_time):
            try:
                time.sleep(1)
                media_name = self.driver.appium_driver.find_element_by_xpath(self.get_media_name_xpath).text
                if media_name is not None:
                    return media_name
            except Exception:
                pass
        else:
            logger.info('Fail to get current media name')
            return None

    def go_to_home_page(self):
        logger.info('go to media streaming page')
        result = self._verify_and_click_element(self.go_to_home_page_xpath)
        if result:
            logger.info('Go to home page successfully')
        else:
            logger.info('Fail to go to home page page')
        return result

    def swip_up(self, t=500, n=1):
        """
        swip up
        :param t: duration, ms
        :param n: times
        :return:
        """
        size = self.driver.appium_driver.get_window_size()
        x1 = size["width"] * 0.5
        y1 = size["height"] * 0.75
        y2 = size["height"] * 0.25
        for i in range(n):
            self.driver.appium_driver.swipe(x1,y1,x1,y2,t)

    def swip_down(self, t=500, n=1):
        """
        swip down
        :param t: duration, ms
        :param n: times
        :return:
        """
        size = self.driver.appium_driver.get_window_size()
        x1 = size["width"] * 0.5
        y1 = size["height"] * 0.25
        y2 = size["height"] * 0.75
        for i in range(n):
            self.driver.appium_driver.swipe(x1, y1, x1, y2, t)

    def close_app(self):
        logger.info('Xiaowei will be closed')
        try:
            self.driver.appium_driver.close_app()
        except Exception as e:
            logger.error(e)
            logger.info('Xiaowei cannot be closed')
            return False
        else:
            logger.info('Xiaowei has been closed successfully')
            return True

    def launch_app(self):
        logger.info('open xiaowei')
        try:
            self.driver.appium_driver.launch_app()
        except Exception as e:
            logger.info('Xiaowei cannnot be opened')
            logger.error(e)
            return False
        else:
            logger.info('Xiaowei has been opened sucessfully')
            return True

    def quit(self):
        logger.info('Quit xiaowei driver')
        try:
            self.driver.appium_driver.quit()
        except Exception as e:
            logger.error(e)
            logger.info('Xiaowei driver cannot be quited')
            return False
        else:
            logger.info('Xiaowei driver has been quited successfully')
            return True

    def verify_device_name(self, dut_name, wait_time=5):
        """
        check headphone name
        :return: True
        """
        try:
            time.sleep(wait_time)
            xiaowei_headphone_name = self.driver.appium_driver.find_element_by_xpath(self.device_name_xpath).text
            dut_name = dut_name.strip()
            xiaowei_headphone_name = xiaowei_headphone_name.strip()
            if xiaowei_headphone_name == dut_name:
                return True
            else:
                logger.error(
                    "dut name is %s, dut name in xiaowei is %s" % (dut_name, xiaowei_headphone_name))
                return False
        except Exception as e:
            logger.error(e)
            return False

    def verify_query_response_text(self, query_text, response_text, response_with_icon=False):
        try:
            wait(1)
            logger.info('Get text of this query %s and response...' % query_text)
            if self.phone_info.phone_type == PhoneType.ANDROID:
                xw_query_response_in_current_page = self.driver.appium_driver.find_elements_by_xpath(self.get_query_response_text)
                if response_with_icon:
                    if "天气" in query_text:
                        xw_last_query_response = xw_query_response_in_current_page[-6:-4]
                    elif "故事" in query_text:
                        xw_last_query_response = xw_query_response_in_current_page[-5:-3]
                    else:
                        xw_last_query_response = None
                elif "翻译" in query_text:
                    xw_last_query_response = xw_query_response_in_current_page[-2:]
                    if query_text == xw_last_query_response[-1].text:
                        logger.info("query text in xiaowei : %s" % xw_last_query_response[-1].text)
                        return True
                    else:
                        if query_text == xw_last_query_response[-2].text and response_text == xw_last_query_response[-1].text:
                            logger.info("query text in xiaowei : %s" % xw_last_query_response[-2].text)
                            logger.info("response text in xiaowei : %s" % xw_last_query_response[-1].text)
                            return True
                    return False
                else:
                    xw_last_query_response = xw_query_response_in_current_page[-2:]
                # logger.info("query text in xiaowei : %s" % xw_last_query_response[0].text)
                # logger.info("response text in xiaowei : %s" % xw_last_query_response[1].text)

            else:
                xw_last_query_response = list()
                if response_with_icon:
                    if "天气" in query_text:
                        xw_query_response_in_current_page = self.driver.appium_driver.find_elements_by_xpath(self.get_query_response_text)
                        xw_last_query_response.append(xw_query_response_in_current_page[-2])
                        xw_last_query_response.append(xw_query_response_in_current_page[-1])
                    elif "故事" in query_text:
                        xw_query_in_current_page = self.driver.appium_driver.find_elements_by_xpath(self.get_query_text)
                        xw_last_query_response.append(xw_query_in_current_page[-2])
                        xw_response_in_current_page = self.driver.appium_driver.find_elements_by_xpath(self.get_response_text)
                        xw_last_query_response.append(xw_response_in_current_page[-2])
                    else:
                        xw_last_query_response = None

                elif "翻译" in query_text:
                    xw_query_in_current_page = self.driver.appium_driver.find_elements_by_xpath(self.get_query_text)
                    xw_last_query_response.append(xw_query_in_current_page[-1])

                    xw_response_in_current_page = self.driver.appium_driver.find_elements_by_xpath(
                        self.get_response_text)
                    if len(xw_response_in_current_page) == 4:
                        xw_last_query_response.append(xw_response_in_current_page[-2])
                    else:
                        xw_last_query_response.append(xw_response_in_current_page[-1])
                else:
                    xw_query_in_current_page = self.driver.appium_driver.find_elements_by_xpath(self.get_query_text)
                    xw_last_query_response.append(xw_query_in_current_page[-1])
                    xw_response_in_current_page = self.driver.appium_driver.find_elements_by_xpath(self.get_response_text)
                    xw_last_query_response.append(xw_response_in_current_page[-1])

            logger.info("query text in xiaowei : %s" % xw_last_query_response[0].text)
            logger.info("response text in xiaowei : %s" % xw_last_query_response[1].text)

            fuzzy_matching_for_query = re.search(repr(query_text), repr(xw_last_query_response[0].text))
            complete_matching_for_query = query_text == xw_last_query_response[0].text
            query_result = fuzzy_matching_for_query or complete_matching_for_query

            fuzzy_matching_for_response = re.search(repr(response_text), repr(xw_last_query_response[1].text))
            complete_matching_for_response = response_text == xw_last_query_response[1].text
            response_result = fuzzy_matching_for_response or complete_matching_for_response

            if query_result and response_result:
                return True
            else:
                return False

        except Exception as e:
            logger.error('Failed to get query and response in xiaowei...')
            return False

    def verify_query_no_response_text(self, query_text):
        wait(2)
        logger.info('Get text of this query %s ...' % query_text)
        if self.phone_info.phone_type == PhoneType.ANDROID:
            xw_query_in_current_page = self.driver.appium_driver.find_elements_by_xpath(self.get_query_response_text)
            count = 0

            xw_last_query = xw_query_in_current_page[-1].text
            if xw_last_query == query_text:
                return xw_last_query
            else:
                for xiaowei_item in xw_query_in_current_page:
                    if xiaowei_item.text.find("你好，我是小微") >= 0:
                        try:
                            logger.info("query text in xiaowei : %s" % xw_query_in_current_page[count+1].text)
                            if count + 1 == len(xw_query_in_current_page):
                                return "录音失败"
                            # elif len(xw_query_in_current_page) > count + 2:
                            #     return "录音失败"
                            else:
                                return xw_query_in_current_page[count+1].text
                        except Exception as e:
                            return "录音失败"
                    else:
                        count += 1
        else:
            try:
                xw_query_in_current_page = self.driver.appium_driver.find_element_by_xpath(self.get_query_text)
            except Exception as e:
                return "录音失败"
            else:
                xw_last_query = xw_query_in_current_page.text
                return xw_last_query

    def activate_activity(self):
        logger.info('Xiaowei app activity will be activate')
        try:
            self.driver.appium_driver.start_activity(self.package_name, self.activity_name)
        except Exception as e:
            logger.error(e)
            logger.info('Xiaowei app activity cannot be activated')
            return False
        else:
            logger.info('Xiaowei app activity has been activated')
            return True

    def activate_app(self):
        logger.info('Xiaowei will be brought to foreground')
        try:
            self.driver.appium_driver.activate_app(self.package_name)
        except Exception as e:
            logger.error(e)
            logger.info('Xiaowei cannot be brought to foreground')
            return False
        else:
            logger.info('Xiaowei has been brought to foreground successfully')
            return True

    def terminate_app(self):
        logger.info('Xiaowei will be terminated')
        try:
            self.driver.appium_driver.terminate_app(self.package_name)
        except Exception as e:
            logger.error(e)
            logger.info('Xiaowei cannot be terminated')
        else:
            logger.info('Xiaowei has been terminated successfully')
        return True

    def lock_screen(self, condition, lock_time):
        logger.info('Screen will be locked')
        try:
            self.driver.appium_driver.lock(lock_time)
        except Exception as e:
            logger.error(e)
        condition.wait()
        self.unlock_screen()
        wait(2)
        self.swip_up(n=2)
        wait(2)
        self.unlock_with_password()
        condition.notify()

    def unlock_screen(self):
        try:
            self.driver.appium_driver.unlock()
        except Exception as e:
            logger.error(e)

    def unlock_with_password(self):
        if self.phone_info.phone_type == PhoneType.IOS:
            self.driver.appium_driver.find_element_by_xpath(self.key2).click()
            wait(0.5)
            self.driver.appium_driver.find_element_by_xpath(self.key6).click()
            wait(0.5)
            self.driver.appium_driver.find_element_by_xpath(self.key7).click()
            wait(0.5)
            self.driver.appium_driver.find_element_by_xpath(self.key3).click()
            wait(0.5)
        else:
            pass

    # *** added by Xinyu *** start
    def wait_till_element_to_be_visible(self, element_xpath, wait_time=2):
        """
        :param self:
        :param element_xpath: target xpath
        :param wait_time: 30ms as default if not specified
        :return:
        """
        try:
            WebDriverWait(self.driver.appium_driver, wait_time, 1).until(
                lambda x: x.find_element_by_xpath(element_xpath))
        except Exception as e:
            logger.exception(e)
            return False
        finally:
            return True


    def wait_find_element(self, element_xpath, wait_time=2):
            element = None
            try:
                isfound = self.wait_till_element_to_be_visible(element_xpath, wait_time)
                if isfound:
                    element = self.driver.appium_driver.find_element_by_xpath(element_xpath)
            except Exception as e:
                pass
            finally:
                return element

    def no_wait_find_element(self, element_xpath):
            element = None
            try:
                element = self.driver.appium_driver.find_element_by_xpath(element_xpath)
            except Exception as e:
                pass
            finally:
                return element

    def wait_find_and_click(self, element_path):
        element = self.wait_find_element(element_path)
        try:
            if element is not None:
                element.click()
                return True
        except Exception as e:
            logger.exception("The element found is not clickable.")
        finally:
            return False

    def no_wait_find_and_click(self, element_path):
        element = self.no_wait_find_element(element_path)
        try:
            if element is not None:
                element.click()
                return True
        except Exception as e:
            logger.exception("The element found is not clickable.")
        finally:
            return False

    # iOS only
    def wechat_login(self):
        """
        only applies to iOS
        wechat login - "微信登录"
        policy agreement - "我已阅读，并同意"
        :return: True on success, False if not prompted
        """

        if not self.wait_find_and_click(self.wechat_login_xpath):
            return False
        self.wait_find_and_click(self.agree_policy_xpath)

        return True

    def allow_alert_window(self):
        """
        look for permission allowing button; click it if found.

        TO DO:
        remove the wait process in iOS scenario

        :return:
        """
        if self.phone_info.phone_type == PhoneType.ANDROID:
            if self.no_wait_find_and_click(self.accept_button_xpath): return True
            if self.no_wait_find_and_click(self.agree_policy_xpath): return True
            if self.no_wait_find_and_click(self.wechat_login_xpath): return True
            if self.no_wait_find_and_click(self.btn_allow_xpath): return True
            if self.no_wait_find_and_click(self.btn_allow_always_xpath): return True
            return False

        if self.phone_info.phone_type == PhoneType.IOS:
            if self.no_wait_find_and_click(self.btn_OK_xpath): return True
            if self.no_wait_find_and_click(self.btn_allow_while_in_use_xpath): return True
            if self.no_wait_find_and_click(self.btn_allow_xpath): return True
            if self.no_wait_find_and_click(self.accept_button_xpath): return True
            if self.no_wait_find_and_click(self.wechat_login_xpath): return True
            if self.no_wait_find_and_click(self.agree_policy_xpath): return True
            return False

    def is_at_main_page(self):
        """
        examine if the main page is visible by checking the existence of record button.
        :return:
        """
        return self.no_wait_find_element(self.btn_record_path)

    # should be run at the start of each launch of Xiaowei
    def grant_permission(self):
        """
        grant permissions at launch of Xiaowei

        :return: True if no exception thrown
        """
        try:
            # keep trying to grant permission until reaches the main page
            # or 5 secs without permission prompt
            cnt = 0
            while not self.is_at_main_page() and cnt < 10:
                if self.allow_alert_window():
                    # reset cnt to 0 when a permission prompt is encountered
                    cnt = 0
                else:
                    # sleep for half a sec if no permission prompt appears
                    time.sleep(0.5)
                    cnt += 1
            return True
            # self.launch_browser()
        except Exception as e:
            logger.exception(e)
        finally:
            return True

    def launch_browser(self):
        if self.phone_info.phone_type == PhoneType.ANDROID:
            if self.phone_info.brand == "HUAWEI":
                package_name = "com.huawei.browser"
                activity_name = "com.huawei.browser.Main"
                self.driver.appium_driver.start_activity(package_name, activity_name)

    def download_from_url(self, url, password):
        pass
        # launch browser
        self.launch_browser()

        # locate search bar
        search_bar = self.wait_find_element(self.homepage_search_bar_xpath)
        if search_bar is not None:
            search_bar.send_keys(url)

        # paste url

        # search

        # locate password bar

        # type password

        # enter

        # locate install and click

        # approve install

        # wait

        # trust immediately

        # trust related developer in setting

    # *** added by Xinyu *** end
