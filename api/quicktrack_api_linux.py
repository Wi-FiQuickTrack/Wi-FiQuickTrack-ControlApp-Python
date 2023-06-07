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
from .quicktrack_api_implementation_interface import QuickTrackApiImplementationInterface
from Commands.ap_commands import *
from Commands.sta_commands import *
from Commands.shared_commands import *
from Commands.afc_commands import *
from api.control_app_helper import ControlAppHelper
from Commands.command import ApiReturnStatus


class QuickTrackApiLinux(QuickTrackApiImplementationInterface):
    """
    class which has inherited the Interface Abstraction Module.
    """

    def start_loop_back_server(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            START_LOOP_BACK_SERVER(tlvs_dict)  # noqa: F405
        )
        return return_status

    def stop_loop_back_server(self):
        return_status = ControlAppHelper.execute_control_app_api(
            STOP_LOOP_BACK_SERVER()  # noqa: F405
        )
        return return_status

    def get_ip_address(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            GET_IP_ADDRESS(tlvs_dict)  # noqa: F405
        )
        return return_status

    def get_mac_address(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            GET_MAC_ADDRESS(tlvs_dict)  # noqa: F405
        )
        return return_status

    def get_dut_app_version_number(self):
        return_status = ControlAppHelper.execute_control_app_api(
            GET_CONTROL_APP_VERSION()  # noqa: F405
        )
        return return_status

    def sta_associate(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_ASSOCIATE(tlvs_dict)  # noqa: F405
        )
        return return_status

    def sta_disconnect(self):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_DISCONNECT()  # noqa: F405
        )
        return return_status


    def create_new_interface_bridge_network(self, tlvs_dict):
        ret_status = ControlAppHelper.execute_control_app_api(
            CREATE_NEW_INTERFACE_BRIDGE_NETWORK(tlvs_dict)
        )
        return ret_status

    def assign_static_ip(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            ASSIGN_STATIC_IP(tlvs_dict)  # noqa: F405
        )
        return return_status

    def sta_configure(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_CONFIGURE(tlvs_dict)  # noqa: F405
        )
        return return_status

    def sta_set_param(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_SET_PARAM(tlvs_dict)
        )
        return return_status

    def sta_send_disconnect(self):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_SEND_DISCONNECT()  # noqa: F405
        )
        return return_status

    def sta_reassociate(self):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_REASSOCIATE()
        )
        return return_status

    def sta_send_btm_query(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_SEND_BTM_QUERY(tlvs_dict)
        )
        return return_status

    def sta_send_anqp_query(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_SEND_ANQP_QUERY(tlvs_dict)
        )
        return return_status

    def p2p_start_up(self):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_START_UP()
        )
        return return_status

    def p2p_find(self):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_FIND()
        )
        return return_status

    def p2p_listen(self):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_LISTEN()
        )
        return return_status

    def p2p_add_group(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_ADD_GROUP(tlvs_dict)
        )
        return return_status

    def p2p_stop_group(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_STOP_GROUP(tlvs_dict)
        )
        return return_status

    def p2p_start_wps(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_START_WPS(tlvs_dict)
        )
        return return_status

    def p2p_connect(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_CONNECT(tlvs_dict)
        )
        return return_status

    def p2p_get_intent_value(self):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_GET_INTENT_VALUE()
        )
        return return_status

    def p2p_invite(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_INVITE(tlvs_dict)
        )
        return return_status

    def p2p_set_serv_disc(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_SET_SERV_DISC(tlvs_dict)
        )
        return return_status

    def p2p_set_ext_listen(self):
        return_status = ControlAppHelper.execute_control_app_api(
            P2P_SET_EXT_LISTEN()
        )
        return return_status

    def device_reset(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            DEVICE_RESET(tlvs_dict)  # noqa: F405
        )
        return return_status

    def start_dhcp(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            START_DHCP(tlvs_dict)
        )
        return return_status

    def stop_dhcp(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            STOP_DHCP(tlvs_dict)
        )
        return return_status

    def get_wsc_pin(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            GET_WSC_PIN(tlvs_dict)
        )
        return return_status

    def ap_configure(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_CONFIGURE(tlvs_dict)
        )
        return return_status

    def ap_set_param(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_SET_PARAM(tlvs_dict)
        )
        return return_status

    def ap_trigger_chanswitch(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_TRIGGER_CHANSWITCH(tlvs_dict)
        )
        return return_status

    def ap_send_btm_req(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_SEND_BTM_REQ(tlvs_dict)
        )
        return return_status

    def ap_start_up(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_START_UP(tlvs_dict)
        )
        return return_status

    def ap_stop(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_STOP(tlvs_dict)
        )
        return return_status

    def ap_send_disconnect(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_SEND_DISCONNECT(tlvs_dict)
        )
        return return_status

    def get_wsc_cred(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            GET_WSC_CRED(tlvs_dict)
        )
        return return_status

    def sta_start_wps(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_START_WPS(tlvs_dict)
        )
        return return_status

    def sta_enable_wsc(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            STA_ENABLE_WSC(tlvs_dict)
        )
        return return_status

    def ap_start_wps(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_START_WPS(tlvs_dict)
        )
        return return_status

    def ap_configure_wsc(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AP_CONFIGURE_WSC(tlvs_dict)
        )
        return return_status

    def afcd_configure(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AFCD_CONFIGURE(tlvs_dict)
        )
        return return_status

    def afcd_operation(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AFCD_OPERATION(tlvs_dict)
        )
        return return_status

    def afcd_get_info(self, tlvs_dict):
        return_status = ControlAppHelper.execute_control_app_api(
            AFCD_GET_INFO(tlvs_dict)
        )
        return return_status
