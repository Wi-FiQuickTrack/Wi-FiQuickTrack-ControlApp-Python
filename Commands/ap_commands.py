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

from .shared_enums import QuickTrackRequestTLV
from .command import ApiInterface, ApiReturnStatus, Command
try:
    from .XXX_ap_command_helper import XXX_ApCommandHelper as ApCommandHelper
except ImportError:
    from .ap_command_helper import ApCommandHelper
import sys
import os
from Commands.dut_logger import DutLogger, LogCategory


class AP_STOP(ApiInterface):
    def execute(self):
        """Method to execute the AP stop command."""
        self.std_out, self.std_err = ApCommandHelper.ap_stop()

    def get_return_status(self):
        """Method to return the return status of AP stop based on the std_err."""
        if self.std_err is None:
            return ApiReturnStatus(0, "AP stop completed : " + str(self.std_out))
        else:
            return ApiReturnStatus(
                1, "Unable to turn off AP.[" + str(self.std_err) + "]"
            )


class AP_START_UP(ApiInterface):
    def execute(self):
        """Method to execute the Access Point start up command."""
        self.std_out, self.std_err = ApCommandHelper.ap_start_up()

    def get_return_status(self):
        """Method to return the return status of AP startup based on the std_err."""
        if self.std_err is None:
            return ApiReturnStatus(0, "AP is up : " + str(self.std_out))
        else:
            return ApiReturnStatus(
                1, "Unable to turn on AP. [" + str(self.std_err) + "]"
            )

tlv_ap_config_mapper = {
    QuickTrackRequestTLV.SSID: "ssid",
    QuickTrackRequestTLV.CHANNEL: "channel",
    QuickTrackRequestTLV.WEP_KEY0: "wep_key0",
    QuickTrackRequestTLV.HW_MODE: "hw_mode",
    QuickTrackRequestTLV.AUTH_ALGORITHM: "auth_algorithm",
    QuickTrackRequestTLV.WEP_DEFAULT_KEY: "wep_default_key",
    QuickTrackRequestTLV.IEEE80211_D: "ieee80211d",
    QuickTrackRequestTLV.IEEE80211_N: "ieee80211n",
    QuickTrackRequestTLV.IEEE80211_AC: "ieee80211ac",
    QuickTrackRequestTLV.COUNTRY_CODE: "country_code",
    QuickTrackRequestTLV.WMM_ENABLED: "wmm_enabled",
    QuickTrackRequestTLV.WPA: "wpa",
    QuickTrackRequestTLV.WPA_KEY_MGMT: "wpa_key_mgmt",
    QuickTrackRequestTLV.RSN_PAIRWISE: "rsn_pairwise",
    QuickTrackRequestTLV.WPA_PASSPHRASE: "wpa_passphrase",
    QuickTrackRequestTLV.WPA_PAIRWISE: "wpa_pairwise",
    QuickTrackRequestTLV.IEEE80211_W: "ieee80211w",
    QuickTrackRequestTLV.IEEE80211_H: "ieee80211h",
    QuickTrackRequestTLV.VHT_OPER_CHWIDTH: "vht_oper_chwidth",
    QuickTrackRequestTLV.IEEE8021_X: "ieee8021x",
    QuickTrackRequestTLV.EAP_SERVER: "eap_server",
    QuickTrackRequestTLV.AUTH_SERVER_ADDR: "auth_server_addr",
    QuickTrackRequestTLV.AUTH_SERVER_PORT: "auth_server_port",
    QuickTrackRequestTLV.AUTH_SERVER_SHARED_SECRET: "auth_server_shared_secret",
    QuickTrackRequestTLV.MBO: "mbo",
    QuickTrackRequestTLV.MBO_CELL_DATA_CONN_PREF: "mbo_cell_data_conn_pref",
    QuickTrackRequestTLV.BSS_TRANSITION: "bss_transition",
    QuickTrackRequestTLV.INTERWORKING: "interworking",
    QuickTrackRequestTLV.RRM_NEIGHBOR_REPORT: "rrm_neighbor_report",
    QuickTrackRequestTLV.RRM_BEACON_REPORT: "rrm_beacon_report",
    QuickTrackRequestTLV.COUNTRY3: "country3",
    QuickTrackRequestTLV.MBO_CELL_CAPA: "mbo_cell_capa",
    QuickTrackRequestTLV.HE_OPER_CHWIDTH: "he_oper_chwidth",
    QuickTrackRequestTLV.SAE_GROUPS: "sae_groups",
    QuickTrackRequestTLV.IEEE80211_AX: "ieee80211ax",
    QuickTrackRequestTLV.SAE_PWE: "sae_pwe",
    QuickTrackRequestTLV.TRANSITION_DISABLE: "transition_disable",
    QuickTrackRequestTLV.OWE_GROUPS: "owe_groups",
    QuickTrackRequestTLV.HE_MU_EDCA: "he_mu_edca",
    QuickTrackRequestTLV.OWE_TRANSITION_BSS_IDENTIFIER: "owe_transition_bss_identifier",
    QuickTrackRequestTLV.IGNORE_BROADCAST_SSID: "ignore_broadcast_ssid",

    QuickTrackRequestTLV.BSS_IDENTIFIER: "bss_identifier",
    QuickTrackRequestTLV.HE_6G_ONLY: "he_6g_only",
    QuickTrackRequestTLV.WSC_CONFIG_ONLY: "wsc_config_only",
    QuickTrackRequestTLV.WPS_ENABLE: "wps_enable",

}
class AP_CONFIGURE(ApiInterface):
    def execute(self):
        """Method to configure the APUT. Configuring the service set identifier (SSID), channel and many more configurations."""
        config = {}
        for tlv_value in self.params:
            config_name = tlv_ap_config_mapper.get(tlv_value)
            if config_name:
                config[config_name] = self.params[tlv_value]
            else:
                self.std_err = "AP configure: Unknown TLV {}".format(tlv_value)
                return

        self.std_out, self.std_err = ApCommandHelper.ap_configure(config)

    def get_return_status(self):
        """Method to return the return status of AP configure based on the std_err."""
        if self.std_err is None:
            return ApiReturnStatus(0, "DUT configured as AP : " + str(self.std_out))
        else:
            return ApiReturnStatus(
                1, "Unable to configure the dut as AP. [" + str(self.std_err) + "]"
            )

tlv_ap_param_mapper = {
    QuickTrackRequestTLV.MBO_ASSOC_DISALLOW: "mbo_assoc_disallow",
    QuickTrackRequestTLV.GAS_COMEBACK_DELAY: "gas_comeback_delay",
}
class AP_SET_PARAM(ApiInterface):
    def execute(self):
        """Method to set run-time parameters to the APUT."""

        param, value = next(iter(self.params.items()))
        param_str = tlv_ap_param_mapper.get(param)
        if param_str is None:
            self.std_err = "The set parameter is not supported"
            return

        result = ApCommandHelper.set_ap_param(param_str, value)
        if "OK" not in result:
            self.std_err = "Unable to set {} {}".format(param_str, value)

    def get_return_status(self):
        """Method to return the return status of AP set parameters based on the std_err."""
        if self.std_err is None:
            return ApiReturnStatus(0, "Set parameter action was successful.")
        else:
            return ApiReturnStatus(
                1, "Unable to set parameters on the AP. [" + str(self.std_err) + "]"
            )


class AP_SEND_DISCONNECT(ApiInterface):
    def execute(self):
        """Method to request a disconnection frame be sent to the given address.
        """
        config = self.params

        try:
            address = config[QuickTrackRequestTLV.ADDRESS]
        except KeyError:
            self.std_err = "AP_SEND_DISCONNECT: required parameter address is missing"
            return

        self.std_out, self.std_err = ApCommandHelper.send_ap_disconnect(address)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully sent disconnection frame"
            )
        else:
            return ApiReturnStatus(
                1,
                "APUT reports problem sending disconnection frame: {}".format(self.std_err)
            )


class AP_SEND_BTM_REQ(ApiInterface):
    def execute(self):
        """Method to trigger BTM Request frame from the Access Point."""
        disassoc_immi = None
        cand_list = None
        disassoc_timer = None
        retry_delay = None
        bss_term_bit = None
        bss_term_tsf = None
        bss_term_duration = None

        bssid = self.params.get(QuickTrackRequestTLV.BSSID)
        if bssid is None:
            self.std_err = "The target BSSID parameter is not specified."
            return

        for key, val in self.params.items():
            if key == QuickTrackRequestTLV.DISASSOC_IMMINENT:
                disassoc_immi = val
            elif key == QuickTrackRequestTLV.BSSID:
                pass
            elif key == QuickTrackRequestTLV.CANDIDATE_LIST:
                cand_list = val
            elif key == QuickTrackRequestTLV.BSS_TERMINATION:
                bss_term_bit = val
            elif key == QuickTrackRequestTLV.DISASSOC_TIMER:
                disassoc_timer = val
            elif key == QuickTrackRequestTLV.BSS_TERMINATION_TSF:
                bss_term_tsf = val
            elif key == QuickTrackRequestTLV.BSS_TERMINATION_DURATION:
                bss_term_duration = val
            elif key == QuickTrackRequestTLV.REASSOCIAITION_RETRY_DELAY:
                retry_delay = val
            else:
                self.std_err = "The parameter {} is not supported in APUT".format(key)
                return

        result = ApCommandHelper.send_ap_btm_req(bssid, disassoc_immi, cand_list, disassoc_timer, retry_delay, bss_term_bit, bss_term_tsf, bss_term_duration)
        if "OK" not in result:
            self.std_err = "Unable to execute Send BTM Req Command"

    def get_return_status(self):
        """Method to return the return status of Triggering BTM request based on the std_err."""
        if self.std_err is None:
            return ApiReturnStatus(0, "Triggering BTM request was successful.")
        else:
            return ApiReturnStatus(
                1, "Unable to trigger BTM request from APUT. [" + str(self.std_err) + "]"
            )


class AP_TRIGGER_CHANSWITCH(ApiInterface):
    def execute(self):
        """Method to set the channel number and frequency on the Access Point."""
        self.channel_num = self.params[QuickTrackRequestTLV.CHANNEL]
        self.frequency = self.params[QuickTrackRequestTLV.FREQUENCY]
        self.std_out, self.std_err = ApCommandHelper.ap_chan_switch(self.channel_num, self.frequency)

    def get_return_status(self):
        """Method to return the return status of Access Point configure channel."""
        if self.std_out is not None:
            if (self.std_out).strip() == "OK":
                return ApiReturnStatus(
                    0,
                    "Channel " + str(self.channel_num) + " successfully configured .",
                )
            else:
                return ApiReturnStatus(
                    1,
                    "Unable to configure channel "
                    + str(self.channel_num)
                    + " .Response received "
                    + str(self.std_out),
                )
        else:
            return ApiReturnStatus(
                2, "Unable to configrue channel on the DUT [" + str(self.std_err) + "]"
            )

class AP_START_WPS(ApiInterface):
    def execute(self):
        """Method to start WPS on STA.
        """

        if QuickTrackRequestTLV.PIN_CODE in self.params:
            pin_code = self.params[QuickTrackRequestTLV.PIN_CODE]
        else:
            pin_code = None

        self.std_out, self.std_err = ApCommandHelper.ap_start_wps(pin_code)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successfully to start WPS on APUT",
            )
        else:
            return ApiReturnStatus(
                1,
                self.std_err
            )

class AP_CONFIGURE_WSC(ApiInterface):
    def execute(self):
        config = {}
        for tlv_value in self.params:
            config_name = tlv_ap_config_mapper.get(tlv_value)
            if config_name:
                config[config_name] = self.params[tlv_value]
            else:
                self.std_err = "AP configure WSC: Unknown TLV {}".format(tlv_value)
                return

        self.std_out, self.std_err = ApCommandHelper.ap_configure_wsc(config)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                self.std_out,
            )
        else:
            return ApiReturnStatus(
                1,
                self.std_err
            )