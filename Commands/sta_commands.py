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
"""Module that contains all the wifi driver commands to be executed."""
from .command import ApiInterface, ApiReturnStatus
try:
    from .XXX_sta_command_helper import XXX_StaCommandHelper as StaCommandHelper
except ImportError:
    from .sta_command_helper import StaCommandHelper
from .command import Command
from .shared_enums import *
import sys
import os
from Commands.dut_logger import DutLogger, LogCategory


class STA_ASSOCIATE(ApiInterface):  # noqa : N801
    """Joins/associates with the station on a linux environment."""

    def execute(self):  # noqa : D1025
        """Method that starts the supplicant to connect to the AP."""
        self.std_err = StaCommandHelper.sta_associate()

    def get_return_status(self):  # noqa : D1025
        """Returns the return status with the status code with following description.

        status code:
        0 - success, Association is complete.
        1 - Failure, Unable to associate.
        2 - Failure, Unable to associate, returns the standard error"""

        if self.std_err is None:
            return ApiReturnStatus(0, "Station was successfully connected to AP. ")
        else:
            return ApiReturnStatus(
                1,
                "The QuickTrack tool was unable to associate. [" + str(self.std_err) + "]",
            )

tlv_sta_config_mapper = {
    QuickTrackRequestTLV.STA_SAE_GROUPS: "sta_sae_groups",
    QuickTrackRequestTLV.MBO_CELL_CAPA: "mbo_cell_capa",
    QuickTrackRequestTLV.SAE_PWE: "sae_pwe",

    QuickTrackRequestTLV.STA_SSID: "sta_ssid",
    QuickTrackRequestTLV.KEY_MGMT: "key_mgmt",
    QuickTrackRequestTLV.STA_WEP_KEY0: "sta_wep_key0",
    QuickTrackRequestTLV.WEP_TX_KEYIDX: "wep_tx_keyidx",
    QuickTrackRequestTLV.GROUP: "group",
    QuickTrackRequestTLV.PSK: "psk",
    QuickTrackRequestTLV.PROTO: "proto",
    QuickTrackRequestTLV.STA_IEEE80211_W: "sta_ieee80211w",
    QuickTrackRequestTLV.PAIRWISE: "pairwise",
    QuickTrackRequestTLV.EAP: "eap",
    QuickTrackRequestTLV.PHASE2: "phase2",
    QuickTrackRequestTLV.PHASE1: "phase1",
    QuickTrackRequestTLV.IDENTITY: "identity",
    QuickTrackRequestTLV.PASSWORD: "password",
    QuickTrackRequestTLV.CA_CERT: "ca_cert",
    QuickTrackRequestTLV.SERVER_CERT: "server_cert",
    QuickTrackRequestTLV.PRIVATE_KEY: "private_key",
    QuickTrackRequestTLV.CLIENT_CERT: "client_cert",
    QuickTrackRequestTLV.DOMAIN_MATCH: "domain_match",
    QuickTrackRequestTLV.DOMAIN_SUFFIX_MATCH: "domain_suffix_match",
    QuickTrackRequestTLV.PAC_FILE: "pac_file",
    QuickTrackRequestTLV.STA_OWE_GROUP: "sta_owe_group",
}
class STA_CONFIGURE(ApiInterface):
    "Configures the STAUT configuration."

    def execute(self):
        "Method to configure the STAUT"
        config = {}
        for tlv_value in self.params:
            config_name = tlv_sta_config_mapper.get(tlv_value)
            if config_name:
                config[config_name] = self.params[tlv_value]
            else:
                self.std_err = "STA configure: Unknown TLV {}".format(tlv_value)
                return
        self.std_out, self.std_err = StaCommandHelper.sta_configure(config)

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, DUT successfully configured.
        1 - Failure, Unable to configure DUT."""

        if self.std_err is None:
            return ApiReturnStatus(0, "STAUT successfully configured")
        else:
            return ApiReturnStatus(
                1, "Unable to configure STAUT {}".format(self.std_err)
            )

class STA_SET_PARAM(ApiInterface):
    "Set run-time parameter to the STAUT."

    def execute(self):
        "Method to set run-time parameter to STAUT."

        param, value = next(iter(self.params.items()))
        param_str = tlv_sta_param_mapper.get(param)
        if param_str is None:
            self.std_err = "The set parameter is not supported in STAUT"
            return

        result = StaCommandHelper.set_sta_param(param_str, value)
        if "OK" not in result:
            self.std_err = "Unable to set {} {}".format(param_str, value)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(0, "Sets run-time parameter to STAUT successfully")
        else:
            return ApiReturnStatus(
                1, "Unable to set run-time parameter to STAUT. [{}]".format(self.std_err)
            )

class STA_DISCONNECT(ApiInterface):  # noqa : N801
    """Class used to disconnect the DUT that is connected."""

    def execute(self):  # noqa : D1025
        """Method used to disconnect the STAUT that is connected to the AP and reset the station back to its normal state after test execution."""

        self.std_out, self.std_err = StaCommandHelper.sta_disconnect()

    def get_return_status(self):  # noqa : D1025
        """Returns the return status with the status code with following description.

        status code:
        0 - success, succussfully disconnected,returns the standard output.
        1- Failure, unable to disconnect, returns the standard error."""
        if self.std_err is None:
            return ApiReturnStatus(
                0, "QuickTrack tool STA was successfully disconnected: " + str(self.std_out)
            )
        else:
            return ApiReturnStatus(
                1,
                "QuickTrack tool STA was unable to disconnect [" + str(self.std_err) + "]",
            )


class STA_SEND_DISCONNECT(ApiInterface):
    def execute(self):
        """Method to request a disconnection frame be sent to the given address.
        """

        self.std_out, self.std_err = StaCommandHelper.send_sta_disconnect()

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully sent disconnection frame"
            )
        else:
            return ApiReturnStatus(
                1,
                "STAUT reports problem sending disconnection frame: {}".format(self.std_err)
            )

class STA_REASSOCIATE(ApiInterface):
    def execute(self):
        """Method to request STA to reassociate with AP.
        """

        self.std_out, self.std_err = StaCommandHelper.sta_reassociate()

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully reassociate with AP"
            )
        else:
            return ApiReturnStatus(
                1,
                "STAUT reports problem when reassociate with AP: {}".format(self.std_err)
            )


class STA_SEND_BTM_QUERY(ApiInterface):
    """Trigger BTM Query frame based on the setting on STAUT"""

    def execute(self):
        """Method to trigger BTM Query frame from STAUT."""
        reason_code = cand_list = None
        for key, val in self.params.items():
            if key == QuickTrackRequestTLV.BTMQUERY_REASON_CODE:
                reason_code  = val
            elif key == QuickTrackRequestTLV.CANDIDATE_LIST:
                cand_list = val
            else:
                self.std_err = "The parameter is not supported in STAUT"
                return

        result = StaCommandHelper.send_sta_btm_query(reason_code, cand_list)
        if "OK" not in result:
            self.std_err = "Unable to execute the command with [{} {}]".format(reason_code, cand_list)

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, Trigger BTM query frame successfully
        1 - Failure, Unable to trigger BTM query frame."""
        if self.std_err is None:
            return ApiReturnStatus(0, "Trigger BTM query frame successfully")
        else:
            return ApiReturnStatus(
                1, "Unable to trigger BTM query frame. [{}]".format(self.std_err)
            )


class STA_SEND_ANQP_QUERY(ApiInterface):
    """Trigger ANQP Query frame based on the setting on STAUT"""

    def execute(self):
        """Method to trigger ANQP Query frame from STAUT."""
        bssid = self.params.get(QuickTrackRequestTLV.BSSID)
        if bssid is None:
            self.std_err = "The target BSSID parameter is not specified."
            return

        for key, val in self.params.items():
            if key == QuickTrackRequestTLV.ANQP_INFO_ID:
                id_param = val
            elif key == QuickTrackRequestTLV.BSSID:
                pass
            else:
                self.std_err = "The parameter {} is not supported in STAUT".format(key)
                return

        result = StaCommandHelper.send_sta_anqp_query(bssid, id_param)
        if "OK" not in result:
            self.std_err = "Unable to execute the command with [{} {}]".format(bssid, id_param)

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, Trigger ANQP query frame successfully
        1 - Failure, Unable to trigger ANQP query frame."""
        if self.std_err is None:
            return ApiReturnStatus(0, "Trigger ANQP query frame successfully")
        else:
            return ApiReturnStatus(
                1, "Unable to trigger ANQP query frame. [{}]".format(self.std_err)
            )
class P2P_START_UP(ApiInterface):
    def execute(self):
        self.std_err =  StaCommandHelper.start_up_p2p()

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(0, "Station was successfully connected to AP. ")
        else:
            return ApiReturnStatus(
                1,
                "The QuickTrack tool was unable to associate. [" + str(self.std_err) + "]",
            )

class P2P_FIND(ApiInterface):
    def execute(self):
        """Method to trigger p2p find.
        """

        self.std_out, self.std_err = StaCommandHelper.p2p_find()

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to start p2p_find"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_FIND API reports problem : {}".format(self.std_err)
            )

class P2P_LISTEN(ApiInterface):
    def execute(self):
        """Method to trigger p2p listen.
        """

        self.std_out, self.std_err = StaCommandHelper.p2p_listen()

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to start p2p_listen"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_LISTEN API reports problem : {}".format(self.std_err)
            )

class P2P_ADD_GROUP(ApiInterface):
    def execute(self):
        """Method to add p2p group.
        """

        if QuickTrackRequestTLV.FREQUENCY in self.params:
            freq = self.params[QuickTrackRequestTLV.FREQUENCY]
        else:
            self.std_err = "Missed TLV: FREQUENCY"
            return
        self.std_out, self.std_err = StaCommandHelper.add_p2p_group(freq)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to add p2p group"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_ADD_GROUP reports problem : {}".format(self.std_err)
            )

class P2P_START_WPS(ApiInterface):
    def execute(self):
        """Method to start WPS on P2P group if.
        """

        if QuickTrackRequestTLV.PIN_CODE in self.params:
            pin_code = self.params[QuickTrackRequestTLV.PIN_CODE]
        else:
            pin_code = None

        # Should use group interface. Choose interface in helper func 
        self.std_out, self.std_err = StaCommandHelper.p2p_start_wps(pin_code)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to start WPS on P2P group if"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_START_WPS reports problem : {}".format(self.std_err)
            )

class P2P_CONNECT(ApiInterface):
    def execute(self):
        """Method to trigger P2P join or GO negotiation.
        """

        if QuickTrackRequestTLV.ADDRESS in self.params:
            mac = self.params[QuickTrackRequestTLV.ADDRESS]
        else:
            self.std_err = "Missed TLV: ADDRESS"
            return
        if QuickTrackRequestTLV.GO_INTENT in self.params:
            intent_value = self.params[QuickTrackRequestTLV.GO_INTENT]
        else:
            intent_value = StaCommandHelper.get_go_intent_value()

        conn_type = None
        if QuickTrackRequestTLV.P2P_CONN_TYPE in self.params:
            conn_type = int(self.params[QuickTrackRequestTLV.P2P_CONN_TYPE])
        he = self.params.get(QuickTrackRequestTLV.IEEE80211_AX, False)
        persist = self.params.get(QuickTrackRequestTLV.PERSISTENT, False)

        pin_code = None    
        if QuickTrackRequestTLV.PIN_CODE in self.params:
            pin_code = self.params[QuickTrackRequestTLV.PIN_CODE]
            if QuickTrackRequestTLV.PIN_METHOD in self.params:
                method = self.params[QuickTrackRequestTLV.PIN_METHOD]
            else:
                self.std_err = "Missed TLV: PIN_METHOD"
                return
        else:
            if QuickTrackRequestTLV.WSC_METHOD in self.params:
                method = self.params[QuickTrackRequestTLV.WSC_METHOD]
            else:
                self.std_err = "Missed TLV: WSC_METHOD"
                return
        self.std_out, self.std_err = StaCommandHelper.p2p_connect(mac, pin_code, method, conn_type, intent_value, he, persist)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to start P2P connect"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_CONNECT reports problem : {}".format(self.std_err)
            )

class P2P_GET_INTENT_VALUE(ApiInterface):
    def execute(self):
        self.std_out = StaCommandHelper.get_go_intent_value()

    def get_return_status(self):
        intent_value = str(self.std_out)
        return ApiReturnStatus(
            0,
            intent_value,
            {QuickTrackResponseTLV.P2P_INTENT_VALUE: intent_value}
        )

class P2P_INVITE(ApiInterface):
    def execute(self):
        if QuickTrackRequestTLV.ADDRESS in self.params:
            mac = self.params[QuickTrackRequestTLV.ADDRESS]
        else:
            self.std_err = "Missed TLV: ADDRESS"
            return
        freq = None
        if QuickTrackRequestTLV.PERSISTENT in self.params:
            persist = True
            freq = self.params.get(QuickTrackRequestTLV.FREQUENCY)
        else:
            persist = False

        # Should use P2P device interface. Choose interface in helper func 
        self.std_out, self.std_err = StaCommandHelper.p2p_invite(mac, persist, freq)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to trigger P2P invitation"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_INVITE reports problem : {}".format(self.std_err)
            )

class P2P_STOP_GROUP(ApiInterface):
    def execute(self):
        if QuickTrackRequestTLV.PERSISTENT in self.params:
            persist = True
        else:
            persist = False
        self.std_out, self.std_err = StaCommandHelper.stop_p2p_group(persist)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to stop P2P group"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_STOP_GROUP reports problem : {}".format(self.std_err)
            )

class P2P_SET_SERV_DISC(ApiInterface):
    def execute(self):
        if QuickTrackRequestTLV.ADDRESS in self.params:
            # Send Service Discovery Req
            addr = self.params[QuickTrackRequestTLV.ADDRESS]
        else:
            # Enable/Add P2P Service
            addr = None

        # Should use P2P device interface. Choose interface in helper func 
        self.std_out, self.std_err = StaCommandHelper.set_p2p_serv_disc(addr)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to set P2P service discovery"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_SET_SERV_DISC reports problem : {}".format(self.std_err)
            )

class P2P_SET_EXT_LISTEN(ApiInterface):
    def execute(self):
        self.std_out, self.std_err = StaCommandHelper.set_p2p_ext_listen()

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to set P2P external listen"
            )
        else:
            return ApiReturnStatus(
                1,
                "P2P_SET_EXT_LISTEN reports problem : {}".format(self.std_err)
            )

class STA_START_WPS(ApiInterface):
    def execute(self):
        """Method to start WPS on STA.
        """

        self.dynamic_pin = False
        if QuickTrackRequestTLV.PIN_CODE in self.params:
            pin_code = self.params[QuickTrackRequestTLV.PIN_CODE]
            if pin_code == "0":
                self.dynamic_pin = True
        else:
            pin_code = None

        self.std_out, self.std_err = StaCommandHelper.sta_start_wps(pin_code)

    def get_return_status(self):
        if self.std_err is None:
            resp_tlvs = None
            if self.dynamic_pin:
                resp_tlvs = {QuickTrackResponseTLV.WSC_PIN_CODE: self.std_out}
            return ApiReturnStatus(
                0,
                "Successfully to start WPS on STAUT",
                resp_tlvs
            )
        else:
            return ApiReturnStatus(
                1,
                "STA_START_WPS reports problem : {}".format(self.std_err)
            )

class STA_ENABLE_WSC(ApiInterface):
    "Configures the STAUT to enable WSC."

    def execute(self):
        "Method to enable WSC in STAUT."
        tlv_wsc_config_mapper = {
            QuickTrackRequestTLV.UPDATE_CONFIG: "update_config",
            QuickTrackRequestTLV.WPS_ENABLE: "wps_enable",
        }
        config = {}
        for tlv_value in self.params:
            config_name = tlv_wsc_config_mapper.get(tlv_value)
            if config_name:
                config[config_name] = self.params[tlv_value]
            else:
                self.std_err = "STA Enable WSC: Unknown TLV {}".format(tlv_value)
                return
        self.std_err = StaCommandHelper.sta_enable_wsc(config)

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, Enable WSC successfully.
        1 - Failure, Unable to enable WSC."""

        if not self.std_err:
            return ApiReturnStatus(0, "STAUT successfully enable WSC")
        else:
            return ApiReturnStatus(
                1, "Unable to enable WSC {}".format(self.std_err)
            )