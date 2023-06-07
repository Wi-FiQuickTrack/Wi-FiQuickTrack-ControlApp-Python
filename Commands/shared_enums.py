# Copyright (c) 2020 Wi-Fi Alliance

# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
# CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
"""Utility module containing all required enum classes."""
from enum import Enum, auto

class CommandOperation(str, Enum):
    """Enum class that defines the network manager state."""

    START = "start"
    STOP = "stop"
    STATUS = "status"


class DutType(Enum):
    """Enum class that defines the DUT type"""

    APUT = 0x02
    STAUT = 0x01
    P2PUT = 0x03


class P2PConnType(Enum):
    """Enum class that defines the P2P connection type"""

    JOIN = 0x01
    AUTH = 0x02

class OperationalBand(Enum):
    """ Enum class that defines the operational band """

    _24GHz = "2.4GHz"
    _5GHz = "5GHz"
    _6GHz = "6GHz"
    dual_band = "dual"

class BssIdentifierBand(Enum):
    _24GHz = 0
    _5GHz = 1
    _6GHz = 2

class DebugLogLevel(Enum):
    DISABLE = 0
    BASIC = 1
    ADVANCED = 2

    @staticmethod
    def get_enum_from_val(value):
        if value == DebugLogLevel.DISABLE.value:
            return DebugLogLevel.DISABLE
        elif value == DebugLogLevel.BASIC.value:
            return DebugLogLevel.BASIC
        else:
            return DebugLogLevel.ADVANCED


class ChannelFreqConfig(Enum):
    """Each configuration enum stores a tuple of channel and its corresponding frequency that will be used to house it."""

    CH_1 = ("1", "2412")
    CH_2 = ("2", "2417")
    CH_3 = ("3", "2422")
    CH_4 = ("4", "2427")
    CH_5 = ("5", "2432")
    CH_6 = ("6", "2437")
    CH_7 = ("7", "2442")
    CH_8 = ("8", "2447")
    CH_9 = ("9", "2452")
    CH_10 = ("10", "2457")
    CH_11 = ("11", "2462")
    # CH_12 = ("12", "2467")
    # CH_13 = ("13", "2472")
    # CH_14 = ("14", "2484")
    CH_36 = ("36", "5180")
    CH_40 = ("40", "5200")
    CH_44 = ("44", "5220")
    CH_48 = ("48", "5240")
    CH_52 = ("52", "5260")
    CH_56 = ("56", "5280")
    CH_60 = ("60", "5300")
    CH_64 = ("64", "5320")
    CH_100 = ("100", "5500")
    CH_104 = ("104", "5520")
    CH_108 = ("108", "5540")
    CH_112 = ("112", "5560")
    CH_116 = ("116", "5580")
    CH_120 = ("120", "5600")
    CH_124 = ("124", "5620")
    CH_128 = ("128", "5640")
    CH_132 = ("132", "5660")
    CH_136 = ("136", "5680")
    CH_140 = ("140", "5700")
    CH_144 = ("144", "5720")
    CH_149 = ("149", "5745")
    CH_153 = ("153", "5765")
    CH_157 = ("157", "5785")
    CH_161 = ("161", "5805")
    CH_165 = ("165", "5825")

    @staticmethod
    def get_24G_channels_frequencies():
        """Returns the list of supported channels in 2.4GHZ operational band"""
        _24G_channels = []
        _24G_frequencies = []
        for each_channel_config in ChannelFreqConfig:
            if int(each_channel_config.value[1]) < 5000:
                _24G_channels.append(each_channel_config.value[0])
                _24G_frequencies.append(each_channel_config.value[1])
        return _24G_channels, _24G_frequencies

    @staticmethod
    def get_5G_channels_frequencies():
        """Returns the list of supported channels in 5GHZ operational band"""
        _5G_channels = []
        _5G_frequencies = []
        for each_channel_config in ChannelFreqConfig:
            if int(each_channel_config.value[1]) > 5000:
                _5G_channels.append(each_channel_config.value[0])
                _5G_frequencies.append(each_channel_config.value[1])
        return _5G_channels, _5G_frequencies

class QuickTrackRequestTLV(int, Enum):
    """List of parameters names that are used in the QuickTrack API request message and
    tool configurations
    """
    SSID = 0x0001
    CHANNEL = 0x0002
    WEP_KEY0 = 0x0003
    AUTH_ALGORITHM = 0x0004
    WEP_DEFAULT_KEY = 0x0005
    IEEE80211_D = 0x0006
    IEEE80211_N = 0x0007
    IEEE80211_AC = 0x0008
    COUNTRY_CODE = 0x0009
    WMM_ENABLED = 0x000a
    WPA = 0x000b
    WPA_KEY_MGMT = 0x000c
    RSN_PAIRWISE = 0x000d
    WPA_PASSPHRASE = 0x000e
    WPA_PAIRWISE = 0x000f
    IEEE80211_H = 0x0011
    IEEE80211_W = 0x0012
    VHT_OPER_CHWIDTH = 0x0013
    IEEE8021_X = 0x0015
    EAP_SERVER = 0x0016
    AUTH_SERVER_ADDR = 0x0017
    AUTH_SERVER_PORT = 0x0018
    AUTH_SERVER_SHARED_SECRET = 0x0019
    INTERFACE_NAME = 0x001a
    NEW_INTERFACE_NAME = 0x001b
    FREQUENCY = 0x001c
    BSS_IDENTIFIER = 0x001d

    HW_MODE = 0x001e
    VHT_OPER_CENTR_FREQ = 0x001f
    RESET = 0x0020
    APP_TYPE = 0x0021
    ADDRESS = 0x0028

    STA_SSID = 0x0035
    KEY_MGMT = 0x0036
    STA_WEP_KEY0 = 0x0037
    WEP_TX_KEYIDX = 0x0038
    GROUP = 0x0039
    PSK = 0x003a
    PROTO = 0x003b
    STA_IEEE80211_W = 0x003c
    PAIRWISE = 0x003d
    EAP = 0x003e
    PHASE2 = 0x003f
    IDENTITY = 0x0040
    PASSWORD = 0x0041
    CA_CERT = 0x0042
    PHASE1 = 0x0043
    CLIENT_CERT = 0x0044
    PRIVATE_KEY = 0x0045

    STATIC_IP = 0x0055
    DEBUG_LEVEL = 0x0057

    #Common params
    HOSTAPD_FILE_NAME = 0x0059
    ROLE = 0x005c
    BAND = 0x005d
    BSSID = 0x005e
    PAC_FILE = 0x006d
    STA_SAE_GROUPS = 0x006e
    SAE_GROUPS = 0x0071
    IEEE80211_AX = 0x0072
    HE_OPER_CHWIDTH = 0x0073
    MBO = 0x0075
    MBO_CELL_DATA_CONN_PREF = 0x0076
    BSS_TRANSITION = 0x0077
    INTERWORKING = 0x0078
    RRM_NEIGHBOR_REPORT = 0x0079
    RRM_BEACON_REPORT = 0x007a
    COUNTRY3 = 0x007b
    MBO_CELL_CAPA = 0x007c
    DOMAIN_MATCH = 0x007d
    DOMAIN_SUFFIX_MATCH = 0x007e
    MBO_ASSOC_DISALLOW = 0x007f
    DISASSOC_IMMINENT = 0x0081
    BSS_TERMINATION = 0x0082
    DISASSOC_TIMER = 0x0083
    BSS_TERMINATION_TSF = 0x0084
    BSS_TERMINATION_DURATION = 0x0085
    REASSOCIAITION_RETRY_DELAY = 0x0086
    BTMQUERY_REASON_CODE = 0x0087
    CANDIDATE_LIST = 0x0088
    ANQP_INFO_ID = 0x0089
    GAS_COMEBACK_DELAY = 0x008a
    SAE_PWE = 0x008d
    OWE_GROUPS = 0x008e
    STA_OWE_GROUP = 0x008f
    HE_MU_EDCA = 0x0090
    TRANSITION_DISABLE = 0x0093
    SERVER_CERT = 0x0099
    OWE_TRANSITION_BSS_IDENTIFIER = 0x00a2
    HE_6G_ONLY = 0x00a6
    GO_INTENT = 0x00c6
    WSC_METHOD = 0x00c7
    PIN_METHOD = 0x00c8
    PIN_CODE = 0x00c9
    P2P_CONN_TYPE = 0x00ca
    WPS_ENABLE = 0x00cc
    UPDATE_CONFIG = 0x00cd
    IGNORE_BROADCAST_SSID = 0x00d1
    PERSISTENT = 0x00d2
    WSC_CONFIG_ONLY = 0x00d3

    ## @brief Defines the version number of the Available Specutrum Inquiry Request
    #  @note TLV Length: Variable, Value: Float - ex: 1.3
    VERSION_NUMBER = 0xB000

    ## @brief Defines Unique ID to identify an instance of an Available Specutrum Inquiry Request
    #  @note TLV Length: Variable, Value: Alphanumeric value
    REQUEST_ID = 0xB001

    ## @brief Defines The derial number of the DUT
    #  @note TLV Length: Variable, Value: Alphanumeric value
    SERIAL_NUMBER = 0xB002

    ## @brief Defines National Regulatory Authority
    #  @note TLV Length: Variable, Value: String - ex: FCC
    NRA = 0XB003

    ## @brief Defines The certification ID of the DUT
    #  @note TLV Length: Variable, Value: Alphanumeric value
    CERT_ID = 0xB004

    ## @brief Defines The identifier of the regulatory rules supported by the DUT
    #  @note TLV Length: Variable, Value: Alphanumeric value
    RULE_SET_ID = 0xB005

    ## @brief Defines Geographic arear within which the DUT is located
    #  @note TLV Length: 0x01, Value: 0: Ellipse 1:LinearPolygon 2: RadialPolygon
    LOCATION_GEO_AREA = 0xB006

    ## @brief Defines The longitude and latitude of the center of DUT ellipse 
    #  @note TLV Length: Variable, Value: "longitude,latitude"
    ELLIPSE_CENTER = 0xB007

    ## @brief Defines The length of the major semi axis of an ellipse within which the DUT is located
    #  @note TLV Length: Variable, Value: Numeric value
    ELLIPSE_MAJOR_AXIS = 0xB008

    ## @brief Defines The length of the minor semi axis of an ellipse within which the DUT is located
    #  @note TLV Length: Variable, Value: Numeric value
    ELLIPSE_MINOR_AXIS = 0xB009

    ## @brief Defines the orientation of the majorAxis field in decimal degrees, measured clockwise from True North
    #  @note TLV Length: 0x01 to 0x03, Value: 0 - 180
    ELLIPSE_ORIENTATION = 0xB00A

    ## @brief Defines the vertices(longitude and latitude) of a polygon within which the DUT is located
    #  @note TLV Length: Variable, Value: longitude,ltitude list with space separate
    LINEARPOLY_BOUNDARY = 0xB00B

    ## @brief Defines The longitude and latitude of the center of DUT RadialPolygon 
    #  @note TLV Length: Variable, Value: "longitude,latitude"
    RADIALPOLY_CENTER = 0xB00C

    ## @brief Defines the vertices(length and angle) of a polygon within which the DUT is located
    #  @note TLV Length: Variable, Value: length,angle list with space separate
    RADIALPOLY_BOUNDARY = 0xB00D

    ## @brief Defines the height of the DUT antenna in meters
    #  @note TLV Length: Variable, Value: Nemeric value

    HEIGHT = 0xB00E
    ## @brief Defines the reference level for the value of the height field
    #  @note TLV Length: Variable, Value: String
    HEIGHT_TYPE = 0xB00F

    ## @brief Defines the height of the DUT antenna in meters
    #  @note TLV Length: Variable, Value: Nemeric value
    VERTICAL_UNCERT = 0xB010

    ## @brief Indicates DUT is indoor deployment
    #  @note TLV Length: 0x01, Value: 0: unknown 1: indoor 2: outdoor
    DEPLOYMENT = 0xB011

    ## @brief Defines Inquired frequency range
    #  @note TLV Length: Variable, Value: lowfreq,highfreq list with space separate
    FREQ_RANGE = 0xB012

    ## @brief Defines Global operating class
    #  @note TLV Length: Variable, Value: Operating class with space separate
    GLOBAL_OPCL = 0xB013
    ## @brief Defines The list of channel center frequency indices
    #  @note TLV Length: Variable, Value: Channel list with space separate
    CHANNEL_CFI = 0xB014
    
    ## @brief Defines minimum Desired EIRP in units of dBm
    #  @note TLV Length: Variable, Value: Numeric value
    MIN_DESIRED_PWR = 0xB015

    ## @brief Defines Field type and payload of a vendor extension
    #  @note TLV Length: Variable, Value: ID: payload
    VENDOR_EXT = 0xB016

    ## @brief Defines the URL of the AFC server
    #  @note TLV Length: Variable, Value: Alphanumeric value
    AFC_SERVER_URL = 0xB017

    ## @brief Defines the SSID to be configured on the DUT
    #  @note TLV Length: 0x00 to 0x1F, Value: Alphanumeric value
    AFC_TEST_SSID = 0xB018

    ## @brief Trigger DUT to its initial pre-test state
    #  @note TLV Length: 0x01, Value: 0(Reserved) or 1
    DEVICE_RESET = 0xB019

    ## @brief Trigger DUT to send Available Spectrum inquiry request
    #  @note TLV Length: 0x01, Value: 0(Default), 1(Channel), 2(Frequency)
    SEND_SPECTRUM_REQ = 0xB01A

    ## @brief Trigger DUT to power cycle
    #  @note TLV Length: 0x01, Value: 0(Reserved) or 1
    POWER_CYCLE = 0xB01B

    ## @brief Specifies Security Configuration
    #  @note TLV Length: 0x01, Value: 0(SAE) or 1(Reserved)
    SECURITY_TYPE = 0xB01C

    ## @brief Defines the pre-shared keys
    #  @note TLV Length: 0x08 to 0xFF, Value: alphanumeric value
    AFC_WPA_PASSPHRASE = 0xB01D

    ## @brief Trigger DUT to send test frames
    #  @note TLV Length: 0x01, Value: 0 - 20MHz, 1 - 40MHz, 2 - 80MHz, 3 - 160MHz, 4 - 320MHz
    SEND_TEST_FRAME = 0xB01E

    ## @brief Specifies DUT's bandwidth
    #  @note TLV Length: 0x01, Value: 0 - 20MHz, 1 - 40MHz, 2 - 80MHz, 3 - 160MHz, 4 - 320MHz
    BANDWIDTH = 0xB01F

    ## @brief Defines the Root certificate file configured on DUT
    #  @note TLV Length: Variable, Value: String
    AFC_CA_CERT = 0xB020

class QuickTrackResponseTLV(int, Enum):
    """List of TLV used in the QuickTrack API response and ACK messages from the DUT"""
    MESSAGE = 0xa000
    STATUS = 0xa001
    DUT_WLAN_IP_ADD = 0xa002
    DUT_MAC_ADD = 0xa003
    QuickTrack_API_VERSION = 0xa004
    LOOP_BACK_SERVER_PORT = 0xa009
    WSC_PIN_CODE = 0xa00a
    P2P_INTENT_VALUE = 0xa00b
    WSC_SSID = 0xa00c
    WSC_WPA_KEY_MGMT = 0xa00d
    WSC_WPA_PASSPHRASE = 0xa00e

    ## @brief Current operating frequency
    #  @note TLV Length: Variable, Value: Numeric value
    OPER_FREQ = 0xBC00

    ## @brief Current operating channel
    #  @note TLV Length: Variable, Value: Numeric value
    OPER_CHANNEL = 0xBC01

class WpsDeviceRole(int, Enum):
    WPS_AP = 0
    WPS_STA = 1