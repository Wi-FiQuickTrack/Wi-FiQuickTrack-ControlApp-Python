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
try:
    from .XXX_command_helper import XXX_CommandHelper as CommandHelper
except ImportError:
    from .command_helper import CommandHelper
from .command import ApiInterface, ApiReturnStatus, Command
from .shared_enums import *
try:
    from .XXX_sta_command_helper import XXX_StaCommandHelper as StaCommandHelper
except ImportError:
    from .sta_command_helper import StaCommandHelper
try:
    from .XXX_ap_command_helper import XXX_ApCommandHelper as ApCommandHelper
except ImportError:
    from .ap_command_helper import ApCommandHelper
import shutil
from loopBackClient.loop_back_client import LoopBackClient
from .dut_logger import DutLogger, LogCategory

loop_back_client = None


class GET_IP_ADDRESS(ApiInterface):
    def execute(self):
        """Method to execute and get the IP address ."""

        std_out, _ = CommandHelper.get_all_interface_ip()
        interface_name = CommandHelper.get_interface_name()
        if CommandHelper.BRIDGE_WLANS in std_out:
            interface_name = CommandHelper.BRIDGE_WLANS
        if QuickTrackRequestTLV.ROLE in self.params:
            role = int(self.params[QuickTrackRequestTLV.ROLE])
            if role == DutType.P2PUT.value:
                interface_name = CommandHelper.get_p2p_group_interface()
        self.std_out = CommandHelper.get_if_ip_addr(interface_name)

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, returns the IP address.
        1- Failure, unable to get the IP address, returns None."""
        if self.std_out is not None:
            ip_address = str(self.std_out)
            return ApiReturnStatus(
                0,
                ip_address,
                {QuickTrackResponseTLV.DUT_WLAN_IP_ADD: ip_address}
            )
        else:
            return ApiReturnStatus(1, str(self.std_out))


class GET_MAC_ADDRESS(ApiInterface):
    def execute(self):
        """Method to execute and get the MAC address."""
        interface_name = CommandHelper.get_interface_name()
        if not self.params:
            self.std_out = CommandHelper.get_if_mac_addr(interface_name)
        else:
            role = self.params[QuickTrackRequestTLV.ROLE]
            band = None
            ssid = None
            bss_identifier = None
            if QuickTrackRequestTLV.BAND in self.params:
                band = self.params[QuickTrackRequestTLV.BAND]
            if QuickTrackRequestTLV.SSID in self.params:
                ssid = self.params[QuickTrackRequestTLV.SSID]
            if QuickTrackRequestTLV.BSS_IDENTIFIER in self.params:
                bss_identifier = int(self.params[QuickTrackRequestTLV.BSS_IDENTIFIER])
            role = int(role)
            if role == DutType.P2PUT.value:
                self.std_out = CommandHelper.get_p2p_mac_addr()
                return

            available_interface_names = CommandHelper.get_all_wlan_name()
            for each_interface in available_interface_names:

                if role == DutType.STAUT.value:
                    interface_freq, interface_ssid, mac_addr = StaCommandHelper.get_sta_if_status(each_interface)
                else:
                    interface_freq, interface_ssid, mac_addr = ApCommandHelper.get_ap_if_status(each_interface)

                if band and ssid:
                    freq_verification_status = CommandHelper.verify_band_from_freq(
                        interface_freq, band
                    )
                    if freq_verification_status:
                        if ssid == interface_ssid:
                            self.std_out = mac_addr
                    else:
                        self.std_err = "Unable to get mac address associated with the given band {}".format(
                            band
                        )
                elif band:
                    freq_verification_status = CommandHelper.verify_band_from_freq(
                        interface_freq, band
                    )
                    if freq_verification_status:
                        self.std_out = mac_addr
                    else:
                        self.std_err = "Unable to get mac address associated with the given band {}".format(
                            band
                        )
                elif ssid:
                    if ssid == interface_ssid:
                        self.std_out = mac_addr
                    else:
                        self.std_err = "Unable to get mac address associated with the given ssid {}".format(
                            ssid
                        )
                elif bss_identifier:
                    identifier = (bss_identifier & 0xF0) >> 4
                    band_bit = bss_identifier & 0x0F
                    operational_band = None
                    if band_bit == BssIdentifierBand._24GHz.value:
                        operational_band = OperationalBand._24GHz.name
                    elif band_bit == BssIdentifierBand._5GHz.value:
                        operational_band = OperationalBand._5GHz.name
                    elif band_bit == BssIdentifierBand._6GHz.value:
                        operational_band = OperationalBand._6GHz.name
                    freq_verification_status = CommandHelper.verify_band_from_freq(
                        interface_freq, operational_band
                    )
                    interface_name = CommandHelper.get_interface_name(identifier)
                    if each_interface == interface_name and freq_verification_status:
                        self.std_out = mac_addr
                    else:
                        self.std_err = "Unable to get mac address associated with the given BSS Identifier {}".format(
                            bss_identifier
                        )
                else:
                    self.std_err = "Unable to get mac address as the required parameters to get the mac address is not passed."

                if self.std_out:
                    break

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, returns the MAC address.
        1- Failure, unable to get the MAC address, returns None."""
        if self.std_out is not None:
            dut_mac_add = str(self.std_out)
            return ApiReturnStatus(
                0,
                dut_mac_add,
                {QuickTrackResponseTLV.DUT_MAC_ADD: dut_mac_add}
            )
        else:
            return ApiReturnStatus(1, str(self.std_err))


class GET_CONTROL_APP_VERSION(ApiInterface):
    def execute(self):
        """Method to execute and get the dut app version number."""
        self.std_out = "v1.0"

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, returns the DUT app version number."""
        supported_api_version = str(self.std_out)
        return ApiReturnStatus(
            0,
            supported_api_version,
            {QuickTrackResponseTLV.QuickTrack_API_VERSION: supported_api_version}
        )


# Deprecated, Tool no longer use this API
class CREATE_NEW_INTERFACE_BRIDGE_NETWORK(ApiInterface):
    """ Class used to create a new interface and a bridge network of existing wireless interface and the new interface created."""

    def execute(self):
        """Method to create the bridged network."""
        bridge_ip = self.params[QuickTrackRequestTLV.STATIC_IP]
        new_interface = self.params[QuickTrackRequestTLV.NEW_INTERFACE_NAME]
        self.std_out, self.std_err = CommandHelper.create_new_interface_bridge_network(
            new_interface
        )

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, returns the bridged network.
        1- Failure, unable to create the bridged network, returns the standard error."""
        if self.std_err is None:
            return ApiReturnStatus(0, "Bridge network is created successfully")
        else:
            return ApiReturnStatus(1, str(self.std_err))


class ASSIGN_STATIC_IP(ApiInterface):
    """ Class used to assign static ip for ethenet and wireless interfaces"""

    def execute(self):
        """Method to assign the static IP for ethernet and wireless interfaces."""
        static_ip = self.params[QuickTrackRequestTLV.STATIC_IP]
        if static_ip:
            self.std_out = CommandHelper.assign_static_ip(static_ip)

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, returns the static ip status.
        1- Failure, unable to set the static ip, returns the standard error."""
        if self.std_out:
            return ApiReturnStatus(
                0, "Static Ip successfully assigned to wireless interface"
            )
        else:
            return ApiReturnStatus(1, "Unable to set static ip.")


class DEVICE_RESET(ApiInterface):
    """ Class used to reset the device """

    def execute(self):
        role = self.params[QuickTrackRequestTLV.ROLE]
        role = int(role)
        interface_name = CommandHelper.get_interface_name()
        debug_log_level = self.params[QuickTrackRequestTLV.DEBUG_LEVEL]
        debug_log_level_enum = DebugLogLevel.get_enum_from_val(int(debug_log_level))

        if role == DutType.STAUT.value:
            StaCommandHelper.set_sta_debug_log_level(debug_log_level_enum)
            self.std_out, self.std_err = StaCommandHelper.sta_disconnect()
            CommandHelper.reset_interface_ip(interface_name)
        elif role == DutType.APUT.value:
            ApCommandHelper.set_ap_debug_log_level(debug_log_level_enum)
            self.std_out, self.std_err = ApCommandHelper.ap_stop()
            CommandHelper.reset_interface_ip(interface_name)
            CommandHelper.reset_bridge_network()
            CommandHelper.clear_bss_identifiers()
        elif role == DutType.P2PUT.value:
            StaCommandHelper.set_sta_debug_log_level(debug_log_level_enum)

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(0, "Device reset successfully")
        else:
            return ApiReturnStatus(1, "Unable to reset the device " + self.std_err)

class START_DHCP(ApiInterface):
    """ API to start DHCP server or client"""
    def execute(self):
        if QuickTrackRequestTLV.ROLE in self.params:
            role = self.params[QuickTrackRequestTLV.ROLE]
            if int(role) == DutType.P2PUT.value:
                if_name = CommandHelper.get_p2p_group_interface()
        else:
            self.std_err = "Missed TLV: ROLE"
            return
        if QuickTrackRequestTLV.STATIC_IP in self.params:
            ip_addr = self.params[QuickTrackRequestTLV.STATIC_IP]
            if ip_addr == "0.0.0.0":
                ip_addr = CommandHelper.DHCP_SERVER_IP
            CommandHelper.assign_static_ip(ip_addr, if_name)
            CommandHelper.start_dhcp_server(if_name, ip_addr)
        else:
            CommandHelper.start_dhcp_client(if_name)
        
    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(0, "Start DHCP successfully")
        else:
            return ApiReturnStatus(1, "Unable to start DHCP " + self.std_err)

class STOP_DHCP(ApiInterface):
    """ API to stop DHCP server or client"""
    def execute(self):
        if QuickTrackRequestTLV.ROLE in self.params:
            role = self.params[QuickTrackRequestTLV.ROLE]
            if int(role) == DutType.P2PUT.value:
                if_name = CommandHelper.get_p2p_group_interface
        else:
            self.std_err = "Missed TLV: ROLE"
            return
        if QuickTrackRequestTLV.STATIC_IP in self.params:
            CommandHelper.stop_dhcp_server()
        else:
            CommandHelper.stop_dhcp_client()

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(0, "Stop DHCP successfully")
        else:
            return ApiReturnStatus(1, "Unable to stop DHCP " + self.std_err)

class GET_WSC_PIN(ApiInterface):
    def execute(self):
        if QuickTrackRequestTLV.ROLE in self.params:
            role = int(self.params[QuickTrackRequestTLV.ROLE])
            if role == DutType.P2PUT.value or role == DutType.STAUT.value:
                self.std_out, self.std_err = StaCommandHelper.get_wsc_pin()
            elif role == DutType.APUT.value:
                self.std_out, self.std_err = ApCommandHelper.get_wsc_pin()
        else:
            self.std_err = "Missed TLV: ROLE"
            return

    def get_return_status(self):
        if self.std_err is None:
            pin_code = str(self.std_out)
            return ApiReturnStatus(
                0,
                pin_code,
                {QuickTrackResponseTLV.WSC_PIN_CODE: pin_code}
            )
        else:
            return ApiReturnStatus(1, str(self.std_err))

class GET_WSC_CRED(ApiInterface):
    def execute(self):
        if QuickTrackRequestTLV.ROLE in self.params:
            role = int(self.params[QuickTrackRequestTLV.ROLE])
            if role == DutType.STAUT.value:
                self.std_out, self.std_err = StaCommandHelper.get_wsc_cred()
            elif role == DutType.APUT.value:
                self.std_out, self.std_err = ApCommandHelper.get_wsc_cred()
        else:
            self.std_err = "Missed TLV: ROLE"
            return

    def get_return_status(self):
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Get WSC credential successfully",
                {QuickTrackResponseTLV.WSC_SSID: self.std_out[0],
                 QuickTrackResponseTLV.WSC_WPA_PASSPHRASE: self.std_out[1],
                 QuickTrackResponseTLV.WSC_WPA_KEY_MGMT: self.std_out[2]}
            )
        else:
            return ApiReturnStatus(1, str(self.std_err))


class START_LOOP_BACK_SERVER(ApiInterface):
    """QuickTrack API for initializing the loopback server.
    Creates a parser for echoing back loop back data to the test tool.
    """

    def execute(self):
        global loop_back_client
        tlv_dict = self.params

        interface_name = None
        std_out, _ = CommandHelper.get_all_interface_ip()
        if CommandHelper.BRIDGE_WLANS in std_out:
            dutIpAddress = CommandHelper.get_if_ip_addr(CommandHelper.BRIDGE_WLANS)
            if dutIpAddress is not None:
                interface_name = CommandHelper.BRIDGE_WLANS
        p2p_group_if = CommandHelper.get_p2p_group_interface()
        if p2p_group_if:
            dutIpAddress = CommandHelper.get_if_ip_addr(p2p_group_if)
            if dutIpAddress is not None:
                interface_name = p2p_group_if
        if interface_name is None:
            interface_name = CommandHelper.get_interface_name()
            dutIpAddress = CommandHelper.get_if_ip_addr(interface_name)
        DutLogger.log(LogCategory.INFO, "Use interface {} for Loopback test".format(interface_name))
 
        if dutIpAddress is not None:
            loop_back_client = LoopBackClient(
                dutIpAddress, 0
            )
            if loop_back_client is None:
                self.std_err = "Failed to initialise loop back server"
            return loop_back_client
        else:
            return ApiReturnStatus(1, "Failed to initialise loopback server")

    def get_return_status(self):
        global loop_back_client
        server_port = loop_back_client.get_port()

        if self.std_err is not None or server_port == 0:
            return ApiReturnStatus(1, "Failed to initialise loop back server")
        else:
            return ApiReturnStatus(
                0,
                "Loop back server initialized",
                {QuickTrackResponseTLV.LOOP_BACK_SERVER_PORT: server_port}
            )

class STOP_LOOP_BACK_SERVER(ApiInterface):
    """QuickTrack API for stopping the loopback server
    """

    def execute(self):
        global loop_back_client
        if loop_back_client is not None:
            loop_back_client.close()
            return True
        else:
            return False

    def get_return_status(self):
        global loop_back_client
        if loop_back_client is not None:
            loop_back_client = None
            return ApiReturnStatus(0, "Loop back server terminated successfully")
        else:
            return ApiReturnStatus(0, "Loopback server in idle state")