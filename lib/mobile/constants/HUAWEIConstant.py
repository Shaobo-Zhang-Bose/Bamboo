#############################################################################
### @brief           HUAWEIConstant
### @author          Shaobo Zhang
### @date            Creation Date: 21/02/2020
###
###  HUAWEIConstant contains All UI locators constants of HUAWEI mobile
###
###
################################################################################


#######################################################################
# List of Constants for Bluetooth  Test Scenario
#######################################################################
# *** added by Xinyu *** start
HOMEPAGE_SEARCH_BAR_XPATH = '//com.huawei.browser[@resource-id="com.huawei.browser:id/homepage_search_bar_text"]'
ALLOW_ALWAYS_XPATH = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_always_button"]'
ALLOW_WHILE_IN_USE_XPATH = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
ALLOW_XPATH = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
# *** added by Xinyu *** end
android_settings_app_package = 'com.android.settings'
android_settings_app_activity = 'com.android.settings.HWSettings'

bluetooth_settings_app_package = 'com.android.settings'
bluetooth_app_activity = 'com.android.settings.Settings$BluetoothSettingsActivity'

location_permission_allow_always_ByXPATH = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_always_button"]'
phone_permission_allow_ByXPATH = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
storage_permission_allow_ByXPATH = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
record_permission_allow_ByXPATH = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
permission_allow_ByXPATH = '//android.widget.Button[contains(@text,"ALLOW") or contains(@text,"Allow")]'

BLUETOOTH_BUTTON_ByXPATH = '//android.widget.TextView[@text="Bluetooth"]'
BLUETOOTH_ON_OFF_CHECK_ByXPATH = '//android.widget.Switch[@resource-id="com.android.settings:id/switch_widget"]'

BLUETOOTH_ON_OFF_ByID = 'com.android.settings:id/switch_widget'
PAIRED_DEVICES_SHOW_MORE_LESS_ByID = 'com.android.settings:id/tv_show_title'

BLUETOOTH_CONNECTED_DEVICE_LIST_ByXPATH = '//android.widget.TextView[' \
                                          'contains(@text,"Connected for")]' \
                                          '/preceding-sibling::android.widget.LinearLayout/android.widget.TextView'

PAIRED_DEVICE_TEXT_ByXPATH = '//android.widget.ImageView[@resource-id="com.android.settings:id/konw_more"]' \
                             '/../preceding-sibling::android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView'

BLUETOOTH_CONNECT_DEVICE_ByXPATH = '//android.widget.TextView[@text="AVAILABLE DEVICES"]' \
                                   '/following::android.widget.LinearLayout/descendant-or-self::android.widget.RelativeLayout/descendant-or-self::android.widget.TextView'

BLUETOOTH_PAIRED_DEVICE_LIST_ByXPATH = '//android.widget.ImageView[@resource-id="com.android.settings:id/konw_more"]'
BLUETOOTH_CONNECTION_SETTINGS_ByID = 'com.android.settings:id/deviceDetails'
BLUETOOTH_UNPAIR_BUTTON_ByXPATH = '//android.widget.Button[@resource-id="com.android.settings:id/unpair_btn"]'
BLUETOOTH_UNPAIR_TEXT_ByXPATH = '//android.widget.TextView[@text="UNPAIR"]'
BLUETOOTH_PAIR_NEW_DEVICE_REFRESH_ByXPATH = '//android.widget.TextView[@resource-id="android:id/title"]'
BLUETOOTH_CONTACT_ACCESS_ALLOW_BUTTON_ByXPATH = '//android.widget.CheckBox[@resource-id="com.android.settings:id/phonebook_sharing_message_confirm_pin"]'
BLUETOOTH_PAIR_BUTTON_ByXPATH = '//android.widget.Button[@resource-id="android:id/button1"]'
BLUETOOTH_PAIR_FAILED_BUTTON_ByXPATH = '//android.widget.Button[@text="OK"]'
BLUETOOTH_DEVICE_NAME_CANCEL_BUTTON_ByXPATH = '//android.widget.Button[@resource-id="com.android.settings:id/cancel_button"]'
BLUETOOTH_DEVICE_SCAN_BAR_ByXPATH = '//android.widget.ProgressBar[@resource-id="com.android.settings:id/scanning_progress"]'
BLUETOOTH_CONNECT_DEVICE_WITH_SCAN_BAR_ByXPATH = '//android.widget.ProgressBar[@resource-id="com.android.settings:id/scanning_progress"]' \
                                                 '/following::android.widget.LinearLayout/descendant::android.widget.RelativeLayout/descendant::android.widget.TextView'

BLUETOOTH_CONNECT_DEVICE_WITH_TITLE_ByXPATH = '//android.widget.TextView[@resource-id="android:id/title"]'

########################################################################################################

BLUETOOTH_ON_OFF_8_0_0_ByXPATH = '//android.widget.Switch'
BLUETOOTH_FORGET_DEVICE_8_1_BUTTON_ByXPATH = '//android.widget.Button[' \
                                             '@text="FORGET DEVICE" or ' \
                                             '@text="Forget device"]'
BLUETOOTH_AVAILABLE_DEVICE_LIST_ByXPATH = '//android.widget.TextView[' \
                                          '@text="Available devices" or ' \
                                          '@text="Pair new device" or ' \
                                          '@text="PAIRED DEVICES" or  ' \
                                          '@text="AVAILABLE ' \
                                          'DEVICES"]/preceding::android.widget.LinearLayout/descendant-or-self::android.widget.RelativeLayout/descendant-or-self::android.widget.TextView'
# BLUETOOTH_CONNECTED_DEVICE_LIST_ByXPATH = '//android.widget.ImageView[@resource-id="android:id/summary"]'

BLUETOOTH_DISCONNECT_DEVICE_ByID = "android:id/button1"
BLUETOOTH_CONNECTION_STATUS_ByXPATH = '//android.widget.TextView[contains(' \
                                      '@text,"Connected")]'
BLUETOOTH_LIST_OF_AVAILABLE_DEVICES_ByXPATH = '//android.widget.TextView[' \
                                              '@text="Available devices" or ' \
                                              '@text="AVAILABLE ' \
                                              'DEVICES"]/following::android.widget.LinearLayout/descendant-or-self::android.widget.RelativeLayout/descendant::android.widget.TextView'
BLUETOOTH_MORE_OPTIONS_ByXPATH = '//android.widget.ImageButton[' \
                                 '@content-desc="More options"]'
BLUETOOTH_RENAME_BUTTON_ByXPATH = '//android.widget.TextView[@text="Rename ' \
                                  'this device"]'
BLUETOOTH_EDIT_TEXTBOX_ByID = 'com.android.settings:id/edittext'
BLUETOOTH_SET_NAME_BUTOON_ByXPATH = '//android.widget.Button[@text="RENAME"]'
BLUETOOTH_DISCONNECT_POP_UP_OK_BUTTON_ByXPATH = '//android.widget.Button[' \
                                                '@text="OK" or ' \
                                                '@text="Disconnect"]'
AVAILABLE_DEVICE_TEXT_ByXPATH = '//android.widget.TextView[@text="Available devices" or @text="AVAILABLE DEVICES"]'

BLUETOOTH_ENABLE_CONTACT_SHARING_BUTTON_ByXPATH = \
    '//android.widget.TextView[@text="Contact sharing"]'
BLUETOOTH_ENABLE_CONTACT_SHARING_CONFIRM_OK_BUTTON_ByXPATH = \
    '//android.widget.Button[@text="OK"]'
BLUETOOTH_DEVICE_TO_CONNECT_AFTER_SWIPE_ByID = 'android:id/title'
BLUETOOTH_POP_UP_OK_BUTTON_ByXPATH = '//android.widget.Button[@text="OK"]'
CONNECTED_DEVICES_BUTTON_ByXPATH = '//android.widget.TextView[' \
                                   '@text="Connected devices" or ' \
                                   '@text="Connections"]'
CONNECTION_REFERENCES_BUTTON_ByXPATH = '//android.widget.TextView[' \
                                       '@text="Connection preferences"]'
BLUETOOTH_DEVICE_SETTINGS_BUTTON_ByID = \
    'com.android.settings:id/settings_button'
BLUETOOTH_DEVICE_SETTINGS_BUTTON_6_0_1_ByID = \
    'com.android.settings:id/deviceDetails'
BLUETOOTH_ENABLE_CONTACT_SHARING_CHECKBOX_ByXPATH = \
    '//android.widget.CheckBox[@text="Contact sharing"]'
BLUETOOTH_ADD_NEW_DEVICE_IN_8_1_ByXPATH = '//android.widget.TextView[' \
                                          '@text="Pair new device"]'
BLUETOOTH_ENABLE_CONTACT_SHARING_SWITCH_IN_8_1_ByXPATH = \
    '//android.widget.TextView[@text="Contact ' \
    'sharing"]/following::android.widget.Switch'
BLUETOOTH_STATUS_SUMMARY_ByXPATH = '//android.widget.TextView[' \
                                   '@text="Pairing…" or ' \
                                   '@text="Connecting…"]'  # ByID =
# 'com.android.settings:id/summary';
BLUETOOTH_FINISH_GOOGLE_ASSISTANT_SETUP_ByXPATH = '//android.widget.Button[' \
                                                  '@text="FINISH SETUP"]'
BLUETOOTH_DONT_ASK_FOR_GA_SETUP_ByXPATH = '//android.widget.Button[contains(' \
                                          '@text,"ASK AGAIN")]'
BLUETOOH_NEXT_BUTTON_GOOGLE_ASSISTANT_ByXPATH = '//android.widget.Button[' \
                                                '@text="NEXT"]'
BLUETOOH_NO_THANKS_BUTTON_GOOGLE_ASSISTANT_ByXPATH = \
    '//android.widget.Button[@text="NO,THANKS"]'
BLUETOOTH_EXIT_GA_SETUP_BUTTON_ByXPATH = \
    '//com.google.android.googlequicksearchbox[@text="EXIT"]'
BLUETOOTH_DONE_BUTTON_GOOGLE_ASSISTANT_ByXPATH = '//android.widget.Button[' \
                                                 '@text="DONE"]'
BLUETOOTH_CONTINUE_BUTTON_ByID = \
    'com.google.android.googlequicksearchbox:id/opa_error_action_button'
BLUETOOTH_MEDIA_VOLUME_SYNC_ByXPATH = '//android.widget.TextView[' \
                                      '@text="Media volume sync"]'
BLUETOOTH_VOLUME_SYNC_SWITCH_ByID = 'com.android.settings:id/switch_bar'
BLUETOOTH_ENABLE_DISABLE_MEDIA_SHARING_ByXPATH = '//android.widget.TextView[' \
                                                 '@text="Media audio"]'
BLUETOOTH_MEDIA_SHARING_SWITCH_ByXPATH = '//android.widget.TextView[' \
                                         '@text="Media ' \
                                         'audio"]/following::android.widget.Switch'
BLUETOOTH_PREVIUSLY_CONNECTED_DEVICE_BUTTON_ByXPATH = \
    '//android.widget.TextView[@text="Previously connected devices" or @text="See all"]'
BLUETOOTH_ANDROID_9_PAIRED_DEVICE_LIST_ByXPATH = '//android.widget.ImageView[@resource-id="com.android.settings:id/konw_more"]'

#######################################################################
# List of Constants for PHone Test Scenario
#######################################################################
ABOUT_PHONE_BUTTON_ByXPATH = '//android.widget.TextView[@text="About phone"]'
STATUS_BUTTON_ByXPATH = '//android.widget.TextView[@text="Status"]'
SERIAL_NUMBER_ByXPATH = '//android.widget.TextView[@text="Serial ' \
                        'number"]/following-sibling::android.widget.TextView'
IMEI_INFORMATION_ByXPATH = '//android.widget.TextView[@text="IMEI ' \
                           'information"]'
IMEI_NUMBER_ByXPATH = '//android.widget.TextView[' \
                      '@text="IMEI"]/following-sibling::android.widget' \
                      '.TextView'
MAC_ADDRESS_NUMBER_ByXPATH = '//android.widget.TextView[contains(@text,' \
                             '"MAC ' \
                             'address")]/following-sibling::android.widget' \
                             '.TextView'
BLUETOOTH_MAC_ADDRESS_ByXPATH = '//android.widget.TextView[contains(@text,' \
                                '"Bluetooth")]/following-sibling::android.widget.TextView'
ALARM_TEXT_ByXPATH = '//android.widget.TextView[@text="Alarm"]'

#######################################################################
# List of Constants for volume Test Scenario
#######################################################################
SOUND_BUTTON_ByXPATH = '//android.widget.TextView[@text="Sound & ' \
                       'notification"]'
MEDIA_VOLUME_ByXPATH = '//android.widget.TextView[@text="Media ' \
                       'volume"]/following::android.widget.SeekBar'

#######################################################################
# List of Constants for Call Test Scenario
#######################################################################
LAUNCH_KEYPAD_ByID = 'com.google.android.dialer:id/floating_action_button'
LAUNCH_KEYPAD_ByXPATH = '//android.widget.ImageButton[@content-desc="key pad"]'
DIAL_BUTTON_ByID = 'com.google.android.dialer:id' \
                   '/dialpad_floating_action_button'
NUMBER_ONE_ByID = 'com.google.android.dialer:id/one'
NUMBER_TWO_ByID = 'com.google.android.dialer:id/two'
NUMBER_THREE_ByID = 'com.google.android.dialer:id/three'
NUMBER_FOUR_ByID = 'com.google.android.dialer:id/four'
NUMBER_FIVE_ByID = 'com.google.android.dialer:id/five'
NUMBER_SIX_ByID = 'com.google.android.dialer:id/six'
NUMBER_SEVEN_ByID = 'com.google.android.dialer:id/seven'
NUMBER_EIGHT_ByID = 'com.google.android.dialer:id/eight'
NUMBER_NINE_ByID = 'com.google.android.dialer:id/nine'
NUMBER_ZERO_ByID = 'com.google.android.dialer:id/zero'
STAR_BUTTON_ByID = 'com.google.android.dialer:id/star'
POUND_BUTTON_ByID = 'com.google.android.dialer:id/pound'
REJECT_CALL_ByXPATH = '//android.widget.Button[@text="Decline" or ' \
                      '@text="DECLINE"]'
ACCEPT_CALL_ByXPATH = '//android.widget.Button[@text="Answer" or ' \
                      '@text="ANSWER"]'
END_CALL_ByID = 'com.google.android.dialer:id/incall_end_call'
MERGE_CALL_ByID = 'com.google.android.dialer:id/incall_fourth_button'

MERGE_CALL_ByXPATH = '//android.widget.TextView[@text="Merge" or @text="MERGE"]'
CALLING_PHONE_STATE_ByXPATH = '//android.widget.TextView[contains(@text,' \
                              '"Calling")]'
INCOMING_PHONE_STATE_ByXPATH = '//android.widget.TextView[contains(@text,' \
                               '"Call from")]'
CALLING_PHONE_STATE_ByID = \
    'com.google.android.dialer:id/contactgrid_status_text'
CALL_SOUND_BUTTON_ByID = 'com.google.android.dialer:id/incall_third_button'
CALL_BLUETOOTH_BUTTON_ByXPATH = '//android.widget.TextView[@text="Bluetooth"]'
CALL_PHONE_BUTTON_ByXPATH = '//android.widget.TextView[@text="Phone"]'
CONFERENCE_CALL_IDENTIFIER_ByXPATH = '//android.widget.TextView'
TIME_ELEMENT_ByID = 'com.google.android.dialer:id/contactgrid_bottom_timer'
ADD_CALL_ByID = 'com.google.android.dialer:id/incall_fourth_button'
PHONE_DIALER_TEXTBOX_ByID = 'com.google.android.dialer:id/digits'
NAVIGATE_TO_CALL_SCREEN_AFTER_ACCEPTING_CALL_USING_MFB_BUTTON_ByXPATH = \
    '//android.widget.TextView[@text="Ongoing call" or @text="On-going call"]'
CREATE_NEW_CONTACT_BUTTON_ByXPATH = '//android.widget.TextView[@text="Create ' \
                                    'new contact" or @text="CREATE CONTACT"]'
FIRST_NAME_BUTTON_TO_ADD_CONTACT_ByXPATH = '//android.widget.EditText[' \
                                           '@text="First name" or ' \
                                           '@text="Name"]'
SAVE_BUTTON_TO_ADD_CONTACT_FOR_ANDROID_6_OR_7_ByXPATH = \
    '//android.widget.Button[@text="SAVE"]'
SAVE_BUTTON_ADD_CONTACT_ByXPATH = '//android.widget.TextView[' \
                                  '@content-desc="Save"]'
VERIFY_CONTACT_ALREADY_EXIST_ByXPATH = '//android.widget.TextView[@text="All contacts" or ' \
                                       '@text="ALL CONTACTS"]'
SELECT_CONTACT_TO_DELETE_ByXPATH = '//android.widget.QuickContactBadge[' \
                                   '@index=0]'
MORE_OPTIONS_TO_DELETE_CONTACT_ByXPATH = '//android.widget.ImageView'
DELETE_OPTIONS_FOR_CONTACT_ByXPATH = '//android.widget.TextView[' \
                                     '@text="Delete"]'
DELETE_BUTTON_FOR_CONTACT_ByXPATH = '//android.widget.Button[@text="DELETE" or @text="delete"' \
                                    'or @text="Delete"]'
ADD_CALL_IN_KEYPAD_ByXPATH = '//android.widget.TextView[@text="Add call"]'
SELECT_CONTACT_SAVE_LOCATION_ByXPATH = '//android.widget.TextView[@text="SIM' \
                                       ' 1"]'
SELECT_DEFAULT_SAVE_LOCATION_ByXPATH = '//android.widget.Button[@text="SET ' \
                                       'AS DEFAULT"]'

#######################################################################
# List of Constants for Music Test Scenario
######################################################################

CONNECT_DEVICE_GET_MUSIC_STATUS_BUTTON_ByXPATH = '//android.widget.ImageButton'
MUSIC_APP_SUBSCRIPTION_CLOSE_BUTTON_ByID = \
    'com.google.android.music:id/modal_header_button'
MUSIC_APP_NO_THANKS_BUTTON_ByXPATH = '//android.widget.Button[@text="NO ' \
                                     'THANKS" or @text="No thanks"]'

# MUSIC_APP_FIRST_SONG_IN_SONGS_LIBRARY_ByXPATH =
# '//android.widget.LinearLayout[@index=2]'
MUSIC_APP_FIRST_SONG_IN_SONGS_LIBRARY_ByID = 'com.google.android.music:id/icon'
# MUSIC_APP_FIRST_SONG_IN_SONGS_LIBRARY_ByXPATH = '//android.view.ViewGroup[
# @index=2]/android.widget.RelativeLayout[
# @index=0]/android.widget.LinearLayout[@index=2 or
# @index=3]/android.widget.LinearLayout[@index=0]'
# MUSIC_APP_FIRST_SONG_IN_SONGS_LIBRARY_ByXPATH = '//android.view.ViewGroup[
# @index=2]/android.widget.RelativeLayout[
# @index=0]/android.widget.LinearLayout[
# @index=1]/android.widget.FrameLayout[@index=1]'
MUSIC_APP_FIRST_SONG_IN_SONGS_LIBRARY_ByXPATH = '//android.view.ViewGroup[' \
                                                '@index=2]/android.widget.RelativeLayout[@index=0]/android.widget.LinearLayout[@index=2 or @index=3]/android.widget.LinearLayout[@index=0]'
MUSIC_APP_SKIP_BUTTON_ByXPATH = '//android.widget.Button[@text="SKIP" or ' \
                                '@text="Skip" or @text="Got it" or @text="NO ' \
                                'THANKS" or @text="No thanks" or @text="GOT ' \
                                'IT" or @text="NO, THANKS" or @text="No, ' \
                                'thanks" or @text="NO,THANKS" or @text="No,' \
                                'thanks" or @text="ALLOW"]'
# MUSIC_APP_NO_THANKS_ByID='com.google.android.music:id/btn_decline'
MUSIC_APP_MENU_BUTTON_FOR_LIBRARIES_ByID = \
    'com.google.android.music:id/navigation_button'
MUSIC_APP_OK_BUTTON_WHEN_NO_INTERNET_CONNECTIVITY_ByXPATH = \
    '//android.widget.Button[@text="OK"]'
MUSIC_APP_NAVIGATION_INSIDE_LIBRARY_ByXPATH = '//android.widget.ImageButton[' \
                                              '@content-desc="Show ' \
                                              'navigation drawer"]'
MUSIC_APP_MUSIC_LIBRARY_IN_MENU_ByXPATH = '//android.widget.TextView[' \
                                          '@text="Music library"]'
MUSIC_APP_SONGS_TAB_BUTTON_ByXPATH = '//android.widget.TextView[@text="SONGS"]'
MUSIC_APP_MINI_PLAYER_ByID = 'com.google.android.music:id/header_text'
MUSIC_APP_CURRENT_SONG_ByID = 'com.google.android.music:id/trackname'
MUSIC_APP_PLAY_PAUSE_ON_MINI_PLAYER_ByID = \
    'com.google.android.music:id/play_pause_header'
# In above content-desc = play or pause
MUSIC_APP_PAUSE_BUTTON_ByID = 'com.google.android.music:id/pause'
MUSIC_APP_NEXT_BUTTON_ByID = 'com.google.android.music:id/next'
MUSIC_APP_PREVIOUS_BUTTON_ByID = 'com.google.android.music:id/prev'
MUSIC_APP_SONG_LIST_ByXPATH = '//android.widget.LinearLayout[' \
                              '@index=2]/android.widget.LinearLayout[' \
                              '@index=0]/android.widget.TextView'
MUSIC_APP_SONG_MORE_INFORMATION_ByID = 'com.google.android.music:id/overflow'
MUSIC_APP_GO_TO_ALBUM_ByXPATH = '//android.widget.TextView[@text="Go to ' \
                                'album"]'
MUSIC_APP_ALBUM_NAME_ByXPATH = '//android.widget.ListView[' \
                               '@index=0]/android.widget.RelativeLayout[' \
                               '@index=0]/android.widget.FrameLayout[' \
                               '@index=1]/android.widget.RelativeLayout[' \
                               '@index=0]/android.widget.TextView[@index=0]'
MUSIC_APP_ARTIST_NAME_ByXPATH = '//android.widget.ListView[' \
                                '@index=0]/android.widget.RelativeLayout[' \
                                '@index=0]/android.widget.FrameLayout[' \
                                '@index=1]/android.widget.RelativeLayout[' \
                                '@index=0]/android.widget.RelativeLayout[' \
                                '@index=1]/android.widget.LinearLayout[' \
                                '@index=0]/android.widget.LinearLayout[' \
                                '@index=1]/android.widget.TextView[@index=0]'
# In above content-desc = play or pause
# MUSIC_APP_PLAY_PAUSE_ON_MINI_PLAYER_ByID =
# 'com.google.android.music:id/play_pause_header'
MUSIC_APP_ANDOIRD_EIGHT_MINI_PLAYER_ByID = \
    'com.google.android.music:id/art_pager'
MUSIC_APP_CURRENT_SONG_TIMER_ByID = 'com.google.android.music:id/currenttime'
MUSIC_APP_GET_CURRENT_SONG_LIST_ByID = 'com.google.android.music:id/icon'
CLEAR_NOTIFICATION_ByXPATH = '//android.widget.ImageView[@resource-id="com.android.systemui:id/delete"]'
CLEAR_NOTIFICATION_ByID = '//"com.android.systemui:id/delete"'

#######################################################################
# List of Constants for BoseConnect Test Scenario
#######################################################################
BOSE_CONNECT_APP_AGREEMENT_AGREE_CHECKBOX_ByID = \
    'com.bose.monet:id/privacy_policy_agreement_checkbox'
BOSE_CONNECT_APP_AGREEMENT_AGREE_BUTTON_ByID = 'com.bose.monet:id/button'
BOSE_CONNECT_APP_GRANT_LOCATION_ACCESS_PERMISSION_TEXT_ByID = \
    'com.bose.monet:id/permissions_header'
BOSE_CONNECT_APP_GRANT_LOCATION_ACCESS_BUTTON_ByID = \
    'com.bose.monet:id/location_access_button'
BOSE_CONNECT_APP_GRANT_DEVICE_LOCATION_BUTTON_ByID = \
    'com.android.packageinstaller:id/permission_allow_button'
BOSE_CONNECT_MENU_ICON_BEFORE_CONNECTION_ByID = \
    'com.bose.monet:id/bose_connect_logo'
BOSE_CONNECT_SETTINGS_BUTTON_ON_HOME_PAGE_ByID = \
    'com.bose.monet:id/settings_icon'
BOSE_CONNECT_DEVICE_UPDATE_WINDOW_NOTHANKS_BUTTON_ByID = \
    'com.bose.monet:id/cancel'
BOSE_CONNECT_APP_CONNECTED_DEVICE_NAME_ByID = \
    'com.bose.monet:id/headphone_name'
BOSE_CONNECT_CLOSE_BUTTON_ByID = 'com.bose.monet:id/close_button'
BOSE_CONNECT_DISCONNECT_BUTTON_ByID = 'com.bose.monet:id/disconnect'
BOSE_CONNECT_CONNECTIONS_IN_SETTINGS_ByID = 'com.bose.monet:id/pdl_container'
BOSE_CONNECT_AUTO_OFF_TIMER_IN_SETTINGS_ByID = \
    'com.bose.monet:id/auto_power_off_container'
BOSE_CONNECT_AUTO_OFF_TIMER_DURATION_ByID = 'com.bose.monet:id/auto_off_time'
BOSE_CONNECT_AUTO_OFF_TIMER_DURATION_RADIO_BUTTON_ByID = \
    'com.bose.monet:id/item_selected'
BOSE_CONNECT_BACK_BUTTON_ByID = 'com.bose.monet:id/back_button'
BOSE_CONNECT_AUTO_OFF_TIMER_DURATION_ByXPATH = \
    '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText'
BOSE_CONNECT_CONNECTIONS_ON_OFF_SWITCH_LIST_ByXPATH = '//android.widget.Switch'
BOSE_CONNECT_CONNECTIONS_DISCONNECT_ByID = 'com.bose.monet:id/yes'
BOSE_CONNECT_CONNECTIONS_PHONE_NAME_ByID = \
    'com.bose.monet:id/name_of_connected_device'
BOSE_CONNECT_PAGE_TITLE_ByID = 'com.bose.monet:id/title'
BOSE_CONNECT_CONNECTIONS_CANCEL_BUTTON_ByID = 'com.bose.monet:id/cancel'
BOSE_CONNECT_CONNECTIONS_CONNECT_NEW_BUTTON_ByID = \
    'com.bose.monet:id/connect_new_device'
BOSE_CONNECT_VOLUME_SLIDER_ByXPATH = '//android.widget.SeekBar'
BOSE_CONNECT_NAME_OF_AVAILABLE_DEVICE_ByID = \
    'com.bose.monet:id/carousel_headphone_name'
BOSE_CONNECT_DEVICE_CONNECTING_MESSAGE_ByID = \
    'com.bose.monet:id/connecting_text'
BOSE_CONNECT_TRY_AGAIN_BUTTON_ByXPATH = '//android.widget.Button[@text="Try ' \
                                        'Again" or @text="TRY AGAIN"]'
BOSE_CONNECT_RENAME_PRODUCT_NAME_TITLE_ByID = \
    'com.bose.monet:id/edit_headphone_title'
BOSE_CONNECT_RENAME_PRODUCT_NAME_TEXTBOX_ByID = 'com.bose.monet:id/edit_name'
BOSE_CONNECT_RENAME_PRODUCT_NAME_CONTINUE_BUTTON_ByID = \
    'com.bose.monet:id/done'
BOSE_CONNECT_MUSIC_SHARING_BUTTON_ByID = 'com.bose.monet:id/music_share_button'
BOSE_CONNECT_MUSIC_SHARING_CONTINUE_ByID = \
    'com.bose.monet:id/music_share_onboarding_continue_button'
BOSE_CONNECT_MUSIC_SHARING_CONTINUE_BUTTON_ByXPATH = \
    '//android.widget.Button[@text="CONTINUE"]'
BOSE_CONNECT_MUSIC_SHARING_GET_STARTED_BUTTON_ByXPATH = \
    '//android.widget.Button[@text="GET STARTED" or @text="Get Started"]'
BOSE_CONNECT_MUSIC_SHARING_PUPPET_STREAMING_MSG_ByXPATH = \
    '//android.widget.TextView[contains(@text,"Streaming to")]'
BOSE_CONNECT_MUSIC_SHARING_PUPPET_SHARING_MSG_ByXPATH = \
    '//android.widget.TextView[contains(@text,"Sharing music")]'
BOSE_CONNECT_MUSIC_SHARING_PUPPET_ByID = \
    'com.bose.monet:id/end_party_mode_layout'
# BOSE_CONNECT_MUSIC_SHARING_PUPPET_ICON_ByID =
# 'com.bose.monet:id/music_share_icon'
BOSE_CONNECT_MUSIC_SHARING_PUPPET_ICON_ByID = \
    'com.bose.monet:id/end_music_share'
BOSE_CONNECT_MUSIC_SHARING_STOP_STREAMING_FROM_SETTINGS_ByID = \
    'com.bose.monet:id/end_music_share'
BOSE_CONNECT_MUSIC_SHARING_DUT_CONNECTING_MESSAGE_ByXPATH = \
    '//android.widget.TextView[contains(@text,"Connecting")]'
BOSE_CONNECT_APP_TRY_AGAIN_BUTTON_ByXPATH = '//android.widget.Button[' \
                                            '@text="Try Again" or @text="TRY' \
                                            ' AGAIN" or @text="OK" or ' \
                                            '@text="ok"]'
BOSE_CONNECT_GET_MUSIC_STATUS_BUTTON_ByXPATH = '//android.widget.ImageButton'
BOSE_CONNECT_APP_OOPS_OK_OR_TRY_AGAIN_BUTTON_ByXPATH = \
    '//android.widget.Button[@text="OK" or @text="ok" or @text="Try Again" ' \
    'or @text="TRY AGAIN"]'
BOSE_CONNECT_PAIRING_ANIMATION_ByID = 'com.bose.monet:id/pairing_message'
BOSE_CONNECT_BLUETOOTH_BUTTON_ON_HOME_PAGE_ByID = \
    'com.bose.monet:id/bluetooth_button'
BOSE_CONNECT_VOICE_PROMPT_TOGGLE_BUTTON_ByID = \
    'com.bose.monet:id/voice_prompt_switch'
BOSE_CONNECT_ACTION_BUTTON_ByID = 'com.bose.monet:id/action_button_container'
BOSE_CONNECT_TOGGLE_OPTION_ByXPATH = '//android.widget.TextView'
BOSE_CONNECT_NOW_PLAYING_ByID = 'com.bose.monet:id/open_now_playing'
BOSE_CONNECT_NOW_PLAYING_ALBUM_NAME_ByID = \
    'com.bose.monet:id/now_playing_album_name'
BOSE_CONNECT_PLAYING_SONG_TITLE_ByID = 'com.bose.monet:id/song_title'
BOSE_CONNECT_PLAYING_SONG_ARTIST_ByID = 'com.bose.monet:id/artist'
BOSE_CONNECT_VOLUME_ROW_SLIDER_ByID = 'com.bose.monet:id/volume_slider'
BOSE_CONNECT_LANGUAGE_SELECT_TEXT_ByXPATH = '//android.widget.TextView[' \
                                            '@text="Language"]'
BOSE_CONNECT_SELECTED_LANGUAGE_TEXT_ByXPATH = \
    '//android.widget.CheckedTextView'
BOSE_CONNECT_LANGUAGE_LIST_ByID = 'android:id/text1'
BOSE_CONNECT_LANGUAGE_SELECT_MENU_ByXPATH = 'android.widget.ListView'
BOSE_CONNECT_CONTINUE_BUTTON_ByID = \
    'com.bose.monet:id/voice_prompt_language_continue_button'
BOSE_CONNECT_PLAY_FLIPPER_ByID = 'com.bose.monet:id/play_flipper'
BOSE_CONNECT_PAUSE_FLIPPER_ByID = 'com.bose.monet:id/pause_flipper'
BOSE_CONNECT_NEXT_ByID = 'com.bose.monet:id/next_btn'
BOSE_CONNECT_PREVIOUS_ByID = 'com.bose.monet:id/previous_btn'
BOSE_CONNECT_CURRENT_SONG_ByID = 'com.bose.monet:id/now_playing_title'

#######################################################################
# List of Constants for Spotify App Test Scenario
#######################################################################

SPOTIFY_FIRST_LOGIN_BUTTON_ByID = 'com.spotify.music:id/button_login'
SPOTIFY_SECOND_LOGIN_BUTTON_ByID = 'com.spotify.music:id/login_button'
SPOTIFY_USERNAME_TEXTBOX_ByID = 'com.spotify.music:id/username_text'
SPOTIFY_PASSWORD_TEXTBOX_ByID = 'com.spotify.music:id/password_text'
SPOTIFY_MENU_BUTTON_ByXPATH = '//android.widget.ImageButton[@content-desc = ' \
                              '"Navigate up"]'
SPOTIFY_BROWSE_BUTTON_ByXPATH = '//android.widget.TextView[@text = "Browse"]'
SPOTIFY_SELECT_SONG_ByXPATH = '//android.widget.RelativeLayout[' \
                              '@index=0]/android.support.v7.widget.RecyclerView[@index=2]/android.widget.LinearLayout[@index=0]/android.widget.ImageView[@index=0]'
SPOTIFY_SHUFFLE_PLAY_ByXPATH = '//android.widget.Button[@text="SHUFFLE PLAY"]'
SPOTIFY_PLAY_PAUSE_BUTTON_IN_MAIN_PLAYER_ByID = 'com.spotify.music:id/btn_play'
SPOTIFY_PLAY_PAUSE_BUTTON_IN_MINI_PLAYER_ByID = \
    'com.spotify.music:id/playPause'
SPOTIFY_NEXT_BUTTON_ByID = 'com.spotify.music:id/btn_next'
SPOTIFY_PREVIOUS_BUTTON_ByID = 'com.spotify.music:id/btn_prev'
SPOTIFY_CURRENT_SONG_NAME_ByXPATH = '//android.widget.FrameLayout[' \
                                    '@index=2]/android.widget.LinearLayout[' \
                                    '@index=0]/android.widget.LinearLayout[' \
                                    '@index=1]/android.widget.TextView[' \
                                    '@index=0]'
SPOTIFY_MINI_PLAYER_ByID = 'com.spotify.music:id/btn_chevron_up'
SPOTIFY_REMIND_ME_LATER_BUTTON_ByID = \
    'com.spotify.music:id/update_later_button'

#######################################################################
# List of Constants for Pandora App Test Scenario - Android
#######################################################################

PANDORA_FIRST_LOGIN_BUTTON_ByID = \
    'com.pandora.android:id/welcome_log_in_button'
PANDORA_EMAIL_TEXTBOX_ByXPATH = '//android.widget.EditText[@text="Email"]'
PANDORA_PASSWORD_TEXTBOX_ByID = 'com.pandora.android:id/password'
PANDORA_SECOND_LOGIN_BUTTON_ByID = \
    'com.pandora.android:id/button_sign_in_submit'
PANDORA_PLAY_PAUSE_BUTTON_ByID = 'com.pandora.android:id/play'
PANDORA_SKIP_BUTTON_ByID = 'com.pandora.android:id/skip_forward'
PANDORA_REPLAY_BUTTON_ByID = 'com.pandora.android:id/replay'
PANDORA_MENU_BUTTON_ByID = 'com.pandora.android:id/toolbar_home'
PANDORA_STATIONS_IN_MENU_ByXPATH = '//android.widget.TextView[' \
                                   '@text="Stations"]'
PANDORA_BROWSE_BUTTON_ByID = 'com.pandora.android:id/right_text'
PANDORA_FIRST_ALBUM_ByXPATH = '//android.widget.FrameLayout[' \
                              '@index=0]/android.widget.LinearLayout[' \
                              '@index=0]/android.widget.RelativeLayout[' \
                              '@index=0]/android.widget.ImageView[@index=0]'
PANDORA_START_THIS_STATION_BUTTON_ByID = \
    'com.pandora.android:id/create_station_button'
PANDORA_MINI_PLAYER_ByID = 'com.pandora.android:id/eq_view'
PANDORA_CURRENT_SONG_NAME_ByID = 'com.pandora.android:id/title'

#######################################################################
# List of Constants for Airplane  Test Scenario
#######################################################################
SETTINGS_MORE_BUTTON_ByXPATH = '//android.widget.TextView[@text="More" or ' \
                               '@text="Network & Internet" or ' \
                               '@text="Connections"]'
AIRPLANE_MODE_ON_OFF_ByID = 'android:id/switch_widget'

####################################################
# List of Constants for Youtube Test Scenario
#######################################################################
YOU_TUBE_APP_SEARCH_BUTTON_ByXPATH = '//android.widget.ImageView[' \
                                     '@content-desc = "Search" or ' \
                                     '@content-desc = "Clear" ]'
YOU_TUBE_SEARCH_TEXT_BOX_ByID = \
    'com.google.android.youtube:id/search_edit_text'
YOU_TUBE_KEY_BOARD_SEARCH_BUTTON_ByXPATH = '//XCUIElementTypeButton[' \
                                           '@name="Search"]'
YOU_TUBE_VIDEO_LIST_ByID = 'com.google.android.youtube:id/video_info_view'
YOUTUBE_VIDEO_PLAYER_ByID = 'com.google.android.youtube:id/subscribe_button'
YOUTUBE_VIDEO_PLAYED_PLAY_PAUSE_BUTTON_ByID = \
    'com.google.android.youtube:id/player_control_play_pause_replay_button'
YOUTUBE_VIDEO_DURATION_ByID = 'com.google.android.youtube:id/thumbnail'
YOUTUBE_VIDEO_COLLAPSE_BUTTON_ByXPATH = '//android.widget.ImageView[' \
                                        '@content-desc = "Minimise"]'
YOUTUBE_VIDEO_MINI_PLAYER_ByXPATH = '//android.widget.HorizontalScrollView[' \
                                    '@index=1 or ' \
                                    '@index=6]/preceding::android.view.ViewGroup[@index=1]'
YOUTUBE_VIDEO_SMALL_SCREEN_ByID = \
    'com.google.android.youtube:id/player_overlays'
YOUTUBE_VIDEO_LIST_ByID = 'com.google.android.youtube:id/title'
YOU_TUBE_SECOND_VIDEO_LIST_ByID = 'com.google.android.youtube:id/duration'
YOUTUBE_WAKE_UP_SCREEN_ByID = \
    'com.google.android.youtube:id/player_fragment_container'

######################################################################
# List of Constants for Call Test Scenario
#######################################################################
SAMSUNG_LAUNCH_KEYPAD_ByID = \
    'com.samsung.android.contacts:id/floating_action_button'
SAMSUNG_DIAL_BUTTON_ByID = 'com.samsung.android.contacts:id/dialButton'
SAMSUNG_NUMBER_ONE_ByID = 'com.samsung.android.contacts:id/one'
SAMSUNG_NUMBER_TWO_ByID = 'com.samsung.android.contacts:id/two'
SAMSUNG_NUMBER_THREE_ByID = 'com.samsung.android.contacts:id/three'
SAMSUNG_NUMBER_FOUR_ByID = 'com.samsung.android.contacts:id/four'
SAMSUNG_NUMBER_FIVE_ByID = 'com.samsung.android.contacts:id/five'
SAMSUNG_NUMBER_SIX_ByID = 'com.samsung.android.contacts:id/six'
SAMSUNG_NUMBER_SEVEN_ByID = 'com.samsung.android.contacts:id/seven'
SAMSUNG_NUMBER_EIGHT_ByID = 'com.samsung.android.contacts:id/eight'
SAMSUNG_NUMBER_NINE_ByID = 'com.samsung.android.contacts:id/nine'
SAMSUNG_NUMBER_ZERO_ByID = 'com.samsung.android.contacts:id/zero'
SAMSUNG_STAR_BUTTON_ByID = 'com.samsung.android.contacts:id/star'
SAMSUNG_POUND_BUTTON_ByID = 'com.samsung.android.contacts:id/pound'
SAMSUNG_REJECT_CALL_ByXPATH = '//android.widget.Button[@text="Decline" or ' \
                              '@text="DECLINE"]'
SAMSUNG_ACCEPT_CALL_ByXPATH = '//android.widget.ImageView[@content-desc= ' \
                              '"Answer"]'
SAMSUNG_END_CALL_ByID = 'com.samsung.android.incallui:id/end_call_button'
SAMSUNG_MERGE_CALL_ByID = \
    'com.samsung.android.contacts:id/incall_fourth_button'
SAMSUNG_CALLING_PHONE_STATE_ByXPATH = '//android.widget.TextView[contains(' \
                                      '@text,"Calling")]'
SAMSUNG_INCOMING_PHONE_STATE_ByXPATH = '//android.widget.TextView[' \
                                       '@text="Incoming call]'
SAMSUNG_CALLING_PHONE_STATE_ByID = \
    'com.samsung.android.contacts:id/contactgrid_status_text'
SAMSUNG_CALL_SOUND_BUTTON_ByID = \
    'com.samsung.android.contacts:id/incall_third_button'
SAMSUNG_CALL_BLUETOOTH_BUTTON_ByXPATH = '//android.widget.TextView[' \
                                        '@text="Bluetooth" or ' \
                                        '@text="bluetooth"]'
SAMSUNG_CALL_PHONE_BUTTON_ByXPATH = '//android.widget.TextView[@text="Phone"]'
SAMSUNG_CONFERENCE_CALL_IDENTIFIER_ByXPATH = '//android.widget.TextView'
SAMSUNG_TIME_ELEMENT_ByID = \
    'com.samsung.android.contacts:id/contactgrid_bottom_timer'
SAMSUNG_ADD_CALL_ByID = 'com.samsung.android.contacts:id/incall_fourth_button'
SAMSUNG_PHONE_DIALER_TEXTBOX_ByID = 'com.samsung.android.contacts:id/digits'
SAMSUNG_NAVIGATE_TO_CALL_SCREEN_AFTER_ACCEPTING_CALL_USING_MFB_BUTTON_ByXPATH \
    = '//android.widget.TextView[@text="Ongoing call" or @text="On-going call"]'
SAMSUNG_CREATE_NEW_CONTACT_BUTTON_ByXPATH = '//android.widget.TextView[' \
                                            '@text="Create new contact"]'
SAMSUNG_FIRST_NAME_BUTTON_TO_ADD_CONTACT_ByXPATH = \
    '//android.widget.TextView[' \
    '@text="Phone"]/preceding-sibling::android.widget.EditText[@text="Name"]'
SAMSUNG_SAVE_BUTTON_TO_ADD_CONTACT_ByXPATH = '//android.widget.Button[' \
                                             '@text="SAVE"]'
SAMSUNG_VERIFY_CONTACT_ALREADY_EXIST_ByXPATH = '//android.widget.TextView[' \
                                               '@text="CONTACTS"]'
SAMSUNG_MORE_OPTIONS_TO_DELETE_CONTACT_ByXPATH = '//android.widget.ImageView'
SAMSUNG_DELETE_OPTIONS_FOR_CONTACT_ByXPATH = '//android.widget.TextView[' \
                                             '@text="Delete"]'
SAMSUNG_DELETE_BUTTON_FOR_CONTACT_ByXPATH = '//android.widget.Button[' \
                                            '@text="DELETE"]'
SAMSUNG_ADD_CALL_IN_KEYPAD_ByXPATH = '//android.widget.TextView[@text="Add ' \
                                     'call"]'
SAMSUNG_SEARCH_CONTACT_ByID = 'android:id/search_src_text'
SAMSUNG_VERIFY_CONTACT_EXIST_ByXPATH = '//android.view.ViewGroup[@index=1]'
SAMSUNG_CONTACT_DETAILS_ByID = 'com.samsung.android.contacts:id/expand_detail'
SAMSUNG_CONTACT_MORE_DETAILS_ByXPATH = '//android.widget.Button[' \
                                       '@content-desc = "More options"]'

#######################################################################
# List of Constants for Bmap  Test Scenario
#######################################################################
PERMISSION_TEXT_VIEW_ByID = 'com.bose.bmap.sample:id/permissions_text_view'
LOCATION_ACCESS_BUTTON_ByID = 'com.bose.bmap.sample:id/location_access_button'
LOCATION_PERMISSION_BUTTON_ByID = \
    'com.bose.bmap.sample:id/location_permission_button'
BLUETOOTH_PERMISSION_BUTTON_ByID = \
    'com.bose.bmap.sample:id/bluetooth_permission_button'
ANDROID_TURN_ON_LOCATION_ByID = 'com.android.settings:id/switch_widget'
APP_GRANT_DEVICE_LOCATION_BUTTON_ByID = \
    'com.android.packageinstaller:id/permission_allow_button'
SEARCH_FOR_AVAILABLE_DEVICE_BUTTON_ByID = 'com.bose.bmap.sample:id/search'
TITLE_OF_DISCOVERY_ByID = 'com.bose.bmap.sample:id/discovery_title'
PAUSE_DISCOVERY_BUTTON_ByID = 'com.bose.bmap.sample:id/pause'
RESTART_DISCOVERY_BUTTON_ByID = 'com.bose.bmap.sample:id/restart'
PRODUCT_NAME_ByID = 'com.bose.bmap.sample:id/product_name'
BLE_CONNECT_AND_DISCONNECT_BUTTON_ByID = 'com.bose.bmap.sample:id/ble_button'
ALL_TAB_ON_PRODUCT_ByID = 'com.bose.bmap.sample:id/psts_tab_title'
OTA_ACTION_BUTTON_ByID = 'com.bose.bmap.sample:id/ota_action_button'
OTA_CURRENT_VERSION_ByID = 'com.bose.bmap.sample:id/ota_current_version'
OTA_CURRENT_STATUS_ICON_ByID = 'com.bose.bmap.sample:id/ota_state_icon'
OTA_CURRENT_STATUS_ByID = 'com.bose.bmap.sample:id/ota_state_title'
OTA_BLUETOOTH_ICON_ByID = 'com.bose.bmap.sample:id/bluetooth_icon'
OTA_NOT_CONNECTED_MESSAGE_ByID = \
    'com.bose.bmap.sample:id/not_connected_message'
OTA_NEW_FW_VERSION_ByID = 'com.bose.bmap.sample:id/ota_new_version'
CUSTOMIZE_OTA_BUTTON_ByID = 'com.bose.bmap.sample:id/ota_custom_url_button'
CUSTOMIZE_FW_URL_ByID = 'com.bose.bmap.sample:id/custom_firmware_url'
CUSTOMIZE_FW_VERSION_ByID = 'com.bose.bmap.sample:id/custom_firmware_version'
CUSTOMIZE_FW_TARGET_EXTERNAL_TOGGLE_ByID = \
    'com.bose.bmap.sample:id/custom_firmware_target_switch'
CUSTOMIZE_FIRMWARE_DOWNLOAD_IMAGE_BUTTON_ByID = \
    'com.bose.bmap.sample:id/custom_firmware_download_button'

#######################################################################
# List of Constants for Madrid  Test Scenario
#######################################################################
MADRID_FIRST_SIGN_IN_BUTTON_ByID = "com.bose.bosemusic.ent.stable:id/login_button"
MADRID_EMAIL_TEXTBOX_ByXPATH = '//android.view.View[@index=3]/preceding::android.widget.EditText'
MADRID_PASSWORD_TEXTBOX_ByXPATH = '//android.view.View[@index=2]/following::android.widget.EditText'
MADRID_SECOND_SIGN_IN_BUTTON_ByXPATH = '//android.widget.Button[@text="Sign In"]'
MADRID_LOCATION_ACCESS_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/round_button'
MADRID_APP_LOCATION_ACCESS_POPUP_BUTTON_ByID = 'com.android.packageinstaller:id/permission_allow_button'
MADRID_SKIP_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/item_skip'
MADRID_PRODUCT_NAME_ByID = 'com.bose.bosemusic.ent.stable:id/device_name'
MADRID_ADD_PRODUCT_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/deviceSelectionButton'
MADRID_PRODUCT_HELP_BUTTON_ByXPATH = '//android.widget.TextView[@text="Product Help"]'
MADRID_CONNECT_PRODUCT_ByXPATH = 'com.bose.bosemusic.ent.stable:id/product_card'
MADRID_IS_PRODUCT_ALREADY_ADDED_SCREEN_ByXPATH = '//android.widget.TextView'
MADRID_PRODUCT_AVAILABILITY_TEXT = 'com.bose.bosemusic.ent.stable:id/availability'
MADRID_MY_BOSE_SCREEN_TEXT = 'com.bose.bosemusic.ent.stable:id/toolbar_title'
MADRID_CONNECT_PRODUCT_BUTTON_ByXPATH = "com.bose.bosemusic.ent.stable:id/placeholder_add_container"
MADRID_ALL_SET_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/product_tour_menu_done_button'
MADRID_SETUP_COMPLETE_TEXT_ByXPATH = '//android.widget.TextView[@text="Setup Complete"]'
MADRID_CONTINUE_BUTTON_ByXPATH = '//android.widget.TextView[@text="Get Started"]'  # com.bose.bosemusic.ent.stable:id/info_message_primaryAction'#com.bose.bosemusic.ent.stable:id/button_text
MADRID_APP_LOADING_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/loading_button'
MADRID_DISMISS_BUTTON_ByXPATH = '//android.widget.TextView[@text="Dismiss"]'
MADRID_APP_PRODUCT_ACTIVATING_TEXT_ByXPATH = '//android.widget.TextView[@text="Activating your product"]'
MADRID_APP_ACTIVATION_SUCCESSFUL_TEXT_ByXPATH = '//android.widget.TextView[@text="Success!"]'
MADRID_GET_CONNECTED_SCREEN_ByXPATH = '//android.widget.TextView[@text="Get Connected"]'
MADRID_APP_ACCOUNT_SETTING_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/item_account_settings'
MADRID_APP_EDIT_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/item_edit'
MADRID_APP_BLUETOOTH_PRODUCT_CHECKBOX_ByXPATH = '//android.widget.TextView[@text="MY BLUETOOTH PRODUCTS"]/following::android.widget.CheckBox'
MADRID_APP_DELETE_PRODUCT_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/item_delete'
MADRID_APP_REMOVE_PRODUCT_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/remove_wifi_product_confirmation'
MADRID_APP_MANAGE_PRODUCT_ByID = 'com.bose.bosemusic.ent.stable:id/drill_down_container'
MADRID_APP_ADDED_PRODUCT_LIST_ByXPATH = '//android.widget.TextView[@text="MY BLUETOOTH PRODUCTS"]/following::android.widget.TextView'
MADRID_APP_PRODUCT_SETTING_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/quick_access_settings'
MADRID_APP_INSTALLING_UPDATE_TEXT_ByID = 'com.bose.bosemusic.ent.stable:id/ota_banner'
MADRID_APP_PRODUCT_CURRENT_FIRMWARE_VERSION_ByXPATH = '//android.widget.TextView[@text="FIRMWARE VERSION"]/following::android.widget.TextView'
MADRID_APP_PRODUCT_NAME_ByXPATH = '//android.widget.ImageView/following::android.widget.TextView'
MADRID_PRODUCT_NAME_OTA_HOME_PAGE_ByID = 'com.bose.bosemusic.ent.stable:id/otg_product_name'
MADRID_APP_APPLY_FIRMWARE_UPDATE_RESTART_NOW_ByID = 'com.bose.bosemusic.ent.stable:id/info_message_primaryAction'
MADRID_APP_PRODUCT_TOUR_BUTTON_ByXPATH = '//android.view.ViewGroup[@content-desc="Got It" or @content-desc="Do it Later"]'  # 'com.bose.bosemusic.ent.stable:id/primary_button'
MADRID_APP_ADD_ANOTHER_PRODUCT_ByXPATH = '//android.widget.ImageButton[@content-desc="Add new product"]'
MADRID_APP_SHORTCUT_BUTTON_ByXPATH = '//android.widget.TextView[@text="Shortcut"]'
MADRID_APP_SETTING_PAGE_PRODUCT_TOUR_ByXPATH = '//android.widget.TextView[@text="Product Tour"]'
MADRID_APP_VOICE_ASSISTANT_ByXPATH = '//android.widget.TextView[@text="Voice Assistant"]'
MADRID_APP_SETTING_PAGE_SELF_VOICE_ByXPATH = '//android.widget.TextView[@text="Self Voice"]'
MADRID_APP_SETTING_NOISE_CANCELLATION_ByXPATH = '//android.widget.TextView[@text="Noise Cancellation"]'
MADRID_APP_SETTING_VOCIE_PROMPTS_ByXPATH = '//android.widget.TextView[@text="Enable Prompts"]/following::android.widget.Switch'
MADRID_SELECT_DEVICE_ASSISTANT_RADIO_BUTTON_ByXPATH = '//android.widget.TextView[@text="Alexa"]/preceding::android.widget.RadioButton'
MADRID_SELECT_ALEXA_AS_VOICE_ASSISTANT_RADIO_ByXPATH = '//android.widget.TextView[@text="Alexa"]/following::android.widget.RadioButton'
MADRID_SELECT_GOOGLE_AS_VOICE_ASSISTANT_RADIO_ByXPATH = '//android.widget.TextView[@text="Google Assistant"]/following::android.widget.RadioButton'
MADRID_SELECT_BATTERY_AS_SHORTCUT_KRY_ByXPATH = '//android.widget.TextView[@text="Enable/Disable Wake Word"]/preceding::android.widget.RadioButton'
MADRID_SELECT_WAKEUP_WORD_AS_SHORTCUT_KRY_ByXPATH = '//android.widget.TextView[@text="Enable/Disable Wake Word"]/following::android.widget.RadioButton'
MADRID_MOISE_CANCELLATION_LEVEL_STATUS = '//android.widget.TextView[@text="Noise Cancellation"]/'
MADRID_BLUETOOTH_CONNECTION_BUTTON_ByXPATH = '//android.widget.TextView[@text="Bluetooth Connections"]'
MADRID_BLUETOOTH_CONNECTION_NEW_ByXPATH = '//android.widget.TextView[@text="Connect New"]'
MADRID_BLUETOOTH_CONNECTION_EDIT_ByXPATH = '//android.widget.TextView[@text="Edit"]'
MADRID_CONNECETED_SOURCE_DEVICE_LIST_ByID = 'com.bose.bosemusic.ent.stable:id/product_connection_name'
MADRID_SET_PRODUCT_CUSTOM_NAME_ByXPATH = '//android.widget.EditText[@text="Custom Name"]'  # 'product_custom_name'
MADRID_SETTING_PAGE_PRODUCT_NAME_TEXT_ByXPATH = '//android.widget.TextView[@text="Product Name"]/following-sibling::android.widget.TextView'
MADRID_SETTING_PAGE_PRODUCT_NAME_ByXPATH = '//android.widget.TextView[@text="Product Name"]'
MADRID_SAVE_CUSTOM_PRODUCT_ByID = 'com.bose.bosemusic.ent.stable:id/button_text'
MADRID_APP_PREDETERMINE_NAMES_ByXPATH = '//android.widget.TextView'
MADRID_APP_TEXT_LIST_ByID = 'com.bose.bosemusic.ent.stable:id/listview_text'
MADRID_APP_RADIO_BUTTON_LIST_ByID = 'com.bose.bosemusic.ent.stable:id/listview_radio'
MADRID_APP_VOICE_ASSISTANT_LIST_ByID = 'com.bose.bosemusic.ent.stable:id/item_text_view'
MADRID_APP_VOICE_ASSISTANT_RADIO_ByID = 'com.bose.bosemusic.ent.stable:id/item_radio_button'
MADRID_APP_AUTOOFF_BUTTON_ByXPATH = '//android.widget.TextView[@text="Auto-Off"]'
MADRID_APP_LANGUAGE_BUTTON_ByXPATH = '//android.widget.TextView[@text="Language"]'
MADRID_APP_SWITCH_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/item_switch'
MADRID_APP_DISCONNECT_DEVICE_BUTTON_ByXPATH = '//android.widget.TextView[@text="Disconnect"]'
MADRID_PRODUCT_NAME_FROM_OTG_PRODUCT_SCREEN_ByID = 'com.bose.bosemusic.ent.stable:id/otg_product_name'
MADRID_QUICK_SOURCE_ACCESS_BUTTON_ByID = 'com.bose.bosemusic.ent.stable:id/quick_access_source'
MADRID_BLUETOOTH_CONNECTION_TITLE_ByXPATH = '//android.widget.TextView[@text="Bluetooth Connections" or @text="Connections"]'
MADRID_NOW_PLAYING_SCREEN_ByID = 'com.bose.bosemusic.ent.stable:id/now_playing_collapsed'