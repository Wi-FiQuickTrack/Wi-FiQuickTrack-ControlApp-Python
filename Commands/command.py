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
"""Module that represents the command format."""
import json
from enum import Enum
from .shared_enums import QuickTrackRequestTLV, QuickTrackResponseTLV
from Commands.dut_logger import DutLogger, LogCategory


class ApiReturnStatus:
    """Class that defines the structure of object that has to be returned by all APIs
    """

    def __init__(self, status: int, message, tlvs = None):
        """Constructore for class ApiReturnStatus

        Parameters
        ----------
        status : int
            status code representing the execution outcome of the command. 0 is successful and any other
            value is a command specific error.
        message : str
            returns message or returns value from the command.
        tlvs : dict
            TLVs returned from the command.
        """
        self.status = status
        self.message = message
        self.tlvs = tlvs
        if tlvs:
            DutLogger.log(LogCategory.INFO, "{}".format(tlvs))

    def to_dict(self):
        tlv_dict = {
            QuickTrackResponseTLV.STATUS: str(self.status),
            QuickTrackResponseTLV.MESSAGE: str(self.message)
        }
        if self.tlvs:
            tlv_dict.update(self.tlvs)
        return tlv_dict

    def get_tlvs_enum(self, tlv_name):
        """Utility method to dynamically get tlvs enum.

        Parameters
        ----------
        tlv_name : [enum]

        Returns
        -------
        AP configuration of TLV.
        """
        try:
            return QuickTrackRequestTLV[tlv_name]
        except Exception:
            pass
        DutLogger.log(LogCategory.ERROR, "TLV not found: " + str(tlv_name))


class ApiInterface:  # pragma: no cover
    """Method to execute the QuickTrack api command."""

    def __init__(self, params: dict = None):
        self.params = params
        self.std_err = None
        self.std_out = None

    def execute(self):
        """Executes the QuickTrack api command."""
        pass

    def get_return_status(self) -> ApiReturnStatus:
        """Gets the return status of the executed QuickTrack api."""
        pass


class Command(str, Enum):
    """Enum class for instructions/commands used to apply  regex and fetch the output."""

    GET_INTERFACE_NAME = "get-interface-name"
    GET_INTERFACE_IP_ADD = "get-interface-ip-address"
    GET_MAC_ADDR = "get-mac-addr"
    GET_CHAN_SWITCH_STATE = "get-channel-switch-status"
    GET_AP_IWDEV_AP_SSID = "get-ap-iwdev-ssid"
    GET_CONNECTED_STA_MAC = "get-connected-sta-mac"
    GET_STA_DUT_MAC_ADDR = "get-sta-dut-mac-addr"
    GET_FREQ = "get-freq"
    GET_STA_SSID = "get-sta-ssid"
    SET_STA_PARAM = "set-sta-param"
    SEND_STA_BTM_QUERY = "send-sta-btm-query"
    SEND_STA_ANQP_QUERY = "send-sta-anqp-query"
    GET_AP_DUT_MAC_ADDR = "get-ap-dut-mac-addr"
    GET_AP_SSID = "get-ap-ssid"
    SET_AP_PARAM = "set-ap-param"
    SEND_AP_BTM_REQ = "send-ap-btm-req"


