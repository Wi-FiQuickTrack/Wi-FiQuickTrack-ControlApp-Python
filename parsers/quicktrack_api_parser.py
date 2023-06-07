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
from parsers.api_parser_interface import ApiParser
from quicktrack_api_message.quicktrack_api_message import QuickTrackAPIMessage, QuickTrackMessageType


class QuickTrackApiParser(ApiParser):
    """
    Parser for decoding QuickTrack APIs

    This parser decodes QuickTrack API's that are sent from the test tool.
    """

    def __init__(self, api_impl):
        self.quicktrack_api_implementation = api_impl

    def decode(self, raw_data):
        """
        Method to decode the QuickTrack API's.

        Decodes the QuickTrack API API's that are sent from the test tool to
        control the dut as per test case requirements.

        Arguments:
            raw_data {string} --string data that is recieved from the client
        """
        quicktrack_api_message = QuickTrackAPIMessage()
        quicktrack_api_message.decode_bytes(raw_data)
        return quicktrack_api_message


    def execute(self, quicktrack_api_message):
        """
        Method to execute the QuickTrack API's.

        executes the required method based on QuickTrack API message sent from the test tool to
        control the dut as per test case requirements.
        """
        command = quicktrack_api_message.message_type
        tlvs_dict = quicktrack_api_message.message_params
        ret_status = None

        #STA
        if command == QuickTrackMessageType.STA_ASSOCIATE:
            ret_status = self.quicktrack_api_implementation.sta_associate(tlvs_dict)
        elif command == QuickTrackMessageType.STA_CONFIGURE:
            ret_status = self.quicktrack_api_implementation.sta_configure(tlvs_dict)
        elif command == QuickTrackMessageType.STA_DISCONNECT:
            ret_status = self.quicktrack_api_implementation.sta_disconnect()
        elif command == QuickTrackMessageType.STA_SEND_DISCONNECT:
            ret_status = self.quicktrack_api_implementation.sta_send_disconnect()
        elif command == QuickTrackMessageType.STA_REASSOCIATE:
            ret_status = self.quicktrack_api_implementation.sta_reassociate()
        elif command == QuickTrackMessageType.STA_SET_PARAM:
            ret_status = self.quicktrack_api_implementation.sta_set_param(tlvs_dict)
        elif command == QuickTrackMessageType.STA_SEND_BTM_QUERY:
            ret_status = self.quicktrack_api_implementation.sta_send_btm_query(tlvs_dict)
        elif command == QuickTrackMessageType.STA_SEND_ANQP_QUERY:
            ret_status = self.quicktrack_api_implementation.sta_send_anqp_query(tlvs_dict)
        elif command == QuickTrackMessageType.P2P_START_UP:
            ret_status = self.quicktrack_api_implementation.p2p_start_up()
        elif command == QuickTrackMessageType.P2P_FIND:
            ret_status = self.quicktrack_api_implementation.p2p_find()
        elif command == QuickTrackMessageType.P2P_LISTEN:
            ret_status = self.quicktrack_api_implementation.p2p_listen()
        elif command == QuickTrackMessageType.P2P_ADD_GROUP:
            ret_status = self.quicktrack_api_implementation.p2p_add_group(tlvs_dict)
        elif command == QuickTrackMessageType.P2P_STOP_GROUP:
            ret_status = self.quicktrack_api_implementation.p2p_stop_group(tlvs_dict)
        elif command == QuickTrackMessageType.P2P_START_WPS:
            ret_status = self.quicktrack_api_implementation.p2p_start_wps(tlvs_dict)
        elif command == QuickTrackMessageType.P2P_CONNECT:
            ret_status = self.quicktrack_api_implementation.p2p_connect(tlvs_dict)
        elif command == QuickTrackMessageType.P2P_GET_INTENT_VLUE:
            ret_status = self.quicktrack_api_implementation.p2p_get_intent_value()
        elif command == QuickTrackMessageType.P2P_INVITE:
            ret_status = self.quicktrack_api_implementation.p2p_invite(tlvs_dict)
        elif command == QuickTrackMessageType.P2P_SET_SERV_DISC:
            ret_status = self.quicktrack_api_implementation.p2p_set_serv_disc(tlvs_dict)
        elif command == QuickTrackMessageType.P2P_SET_EXT_LISTEN:
            ret_status = self.quicktrack_api_implementation.p2p_set_ext_listen()
        elif command == QuickTrackMessageType.STA_START_WPS:
            ret_status = self.quicktrack_api_implementation.sta_start_wps(tlvs_dict)
        elif command == QuickTrackMessageType.STA_ENABLE_WSC:
            ret_status = self.quicktrack_api_implementation.sta_enable_wsc(tlvs_dict)
        #Common
        elif command == QuickTrackMessageType.GET_IP_ADDR:
            ret_status = (self.quicktrack_api_implementation.get_ip_address(tlvs_dict))
        elif command == QuickTrackMessageType.GET_MAC_ADDR:
            ret_status = (self.quicktrack_api_implementation.get_mac_address(tlvs_dict))
        elif command == QuickTrackMessageType.GET_CONTROL_APP_VERSION:
            ret_status = (self.quicktrack_api_implementation.get_dut_app_version_number())
        if command == QuickTrackMessageType.START_LOOP_BACK_SERVER:
            ret_status = self.quicktrack_api_implementation.start_loop_back_server(tlvs_dict)
        elif command == QuickTrackMessageType.STOP_LOOP_BACK_SERVER:
            ret_status = self.quicktrack_api_implementation.stop_loop_back_server()
        elif command == QuickTrackMessageType.CREATE_NEW_INTERFACE_BRIDGE_NETWORK:
            ret_status = self.quicktrack_api_implementation.create_new_interface_bridge_network(tlvs_dict)
        elif command == QuickTrackMessageType.ASSIGN_STATIC_IP:
            ret_status = self.quicktrack_api_implementation.assign_static_ip(tlvs_dict)
        elif command == QuickTrackMessageType.DEVICE_RESET:
            ret_status = self.quicktrack_api_implementation.device_reset(tlvs_dict)
        elif command == QuickTrackMessageType.START_DHCP:
            ret_status = self.quicktrack_api_implementation.start_dhcp(tlvs_dict)
        elif command == QuickTrackMessageType.STOP_DHCP:
            ret_status = self.quicktrack_api_implementation.stop_dhcp(tlvs_dict)
        elif command == QuickTrackMessageType.GET_WSC_PIN:
            ret_status = self.quicktrack_api_implementation.get_wsc_pin(tlvs_dict)
        elif command == QuickTrackMessageType.GET_WSC_CRED:
            ret_status = self.quicktrack_api_implementation.get_wsc_cred(tlvs_dict)
        #AP
        elif command == QuickTrackMessageType.AP_START_UP:
            ret_status = self.quicktrack_api_implementation.ap_start_up(tlvs_dict)
        elif command == QuickTrackMessageType.AP_STOP:
            ret_status = self.quicktrack_api_implementation.ap_stop(tlvs_dict)
        elif command == QuickTrackMessageType.AP_CONFIGURE:
            ret_status = self.quicktrack_api_implementation.ap_configure(tlvs_dict)
        elif command == QuickTrackMessageType.AP_TRIGGER_CHANSWITCH:
            ret_status = self.quicktrack_api_implementation.ap_trigger_chanswitch(tlvs_dict)
        elif command == QuickTrackMessageType.AP_SEND_DISCONNECT:
            ret_status = self.quicktrack_api_implementation.ap_send_disconnect(tlvs_dict)
        elif command == QuickTrackMessageType.AP_SET_PARAM:
            ret_status = self.quicktrack_api_implementation.ap_set_param(tlvs_dict)
        elif command == QuickTrackMessageType.AP_SEND_BTM_REQ:
            ret_status = self.quicktrack_api_implementation.ap_send_btm_req(tlvs_dict)
        elif command == QuickTrackMessageType.AP_START_WPS:
            ret_status = self.quicktrack_api_implementation.ap_start_wps(tlvs_dict)
        elif command == QuickTrackMessageType.AP_CONFIGURE_WSC:
            ret_status = self.quicktrack_api_implementation.ap_configure_wsc(tlvs_dict)
        elif command == QuickTrackMessageType.AFCD_CONFIGURE:
            ret_status = self.quicktrack_api_implementation.afcd_configure(tlvs_dict)
        elif command == QuickTrackMessageType.AFCD_OPERATION:
            ret_status = self.quicktrack_api_implementation.afcd_operation(tlvs_dict)
        elif command == QuickTrackMessageType.AFCD_GET_INFO:
            ret_status = self.quicktrack_api_implementation.afcd_get_info(tlvs_dict)
        return ret_status
