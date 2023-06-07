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
"""@package quicktrack_message.py : Contains the object used to store QuickTrack API message.

Contains the class used to represent an QuickTrack API message that is used for communication with the DUT control application."""
from Commands.shared_enums import QuickTrackRequestTLV, QuickTrackResponseTLV
from enum import Enum
from Commands.dut_logger import DutLogger, LogCategory

QuickTrack_MESSAGE_VERSION = 0x01
class QuickTrackMessageType(Enum):
    """Enum class QuickTrack API command discriptor.

    Enums that define each of the QuickTrack API command, The same values are used by the DUT to decode the command being sent.
    """

    CMD_RESPONSE = 0x0000
    CMD_ACK = 0x0001

    AP_START_UP = 0x1000
    AP_STOP = 0x1001
    AP_CONFIGURE = 0x1002
    AP_TRIGGER_CHANSWITCH = 0x1003
    AP_SEND_DISCONNECT = 0x1004
    AP_SET_PARAM = 0x1005
    AP_SEND_BTM_REQ = 0x1006
    AP_START_WPS = 0x1008
    AP_CONFIGURE_WSC = 0x1009

    STA_ASSOCIATE = 0x2000
    STA_CONFIGURE = 0x2001
    STA_DISCONNECT = 0x2002
    STA_SEND_DISCONNECT = 0x2003
    STA_REASSOCIATE = 0x2004
    STA_SET_PARAM = 0x2005
    STA_SEND_BTM_QUERY = 0x2006
    STA_SEND_ANQP_QUERY = 0x2007
    P2P_START_UP = 0x200C
    P2P_FIND = 0x200D
    P2P_LISTEN = 0x200E
    P2P_ADD_GROUP = 0x200F
    P2P_START_WPS = 0x2010
    P2P_CONNECT = 0x2011
    P2P_GET_INTENT_VLUE = 0x2015
    STA_START_WPS = 0x2016
    P2P_INVITE = 0x2018
    P2P_STOP_GROUP = 0x2019
    P2P_SET_SERV_DISC = 0x201A
    P2P_SET_EXT_LISTEN = 0x201C
    STA_ENABLE_WSC = 0x201D

    GET_IP_ADDR = 0x5000
    GET_MAC_ADDR = 0x5001
    GET_CONTROL_APP_VERSION = 0x5002
    START_LOOP_BACK_SERVER = 0x5003
    STOP_LOOP_BACK_SERVER = 0x5004
    CREATE_NEW_INTERFACE_BRIDGE_NETWORK = 0x5005
    ASSIGN_STATIC_IP = 0x5006
    DEVICE_RESET = 0x5007
    START_DHCP = 0x500A
    STOP_DHCP = 0x500B
    GET_WSC_PIN = 0x500C
    GET_WSC_CRED = 0x500D

    AFCD_CONFIGURE = 0x6001
    AFCD_OPERATION = 0x6002
    AFCD_GET_INFO = 0x6003

class QuickTrackAPIMessage():

    def __init__(self, message_type: QuickTrackMessageType=None, message_params: dict=None):
        """Constructor for class QuickTrackAPIMessage.

        Parameters
        ----------
        message_type : QuickTrackMessageType, optional
            Type of QuickTrack API message, by default None
        message_params : dict, optional
            QuickTrack API message parameters, by default {}
        """
        self.message_version = QuickTrack_MESSAGE_VERSION
        self.message_type = message_type
        self.message_id = 0
        self.message_params = message_params

    def set_message_id(self, message_id: int):
        """Sets QuickTrack message id before transmission over control path

        Parameters
        ----------
        message_id : int
            ID for the message being transmitted
        """
        if message_id > 0xFFFF:
            DutLogger.log(LogCategory.ERROR, "Message id should be in the rage of 0 to 0xFFFF")
            return
        self.message_id = message_id

    def get_message_bytes(self):
        """Method to convert the QuickTrack message to bytearray for transmission over control path.

        Returns
        -------
        bytearray
            byte array representation of the QuickTrack message
        """
        try:
            message_bytes = bytearray()
            message_bytes.append(self.message_version)
            message_bytes.extend(self.message_type.value.to_bytes(2, byteorder='big'))
            message_bytes.extend(self.message_id.to_bytes(2, byteorder='big'))
            message_bytes.extend([0xFF, 0xFF]) #Reserved 2 octets

            if self.message_params:
                for param in self.message_params:
                    param_tlv = self.__get_tlv_byte_array(int(param.value), str(self.message_params[param]))
                    message_bytes.extend(param_tlv)
            return message_bytes
        except Exception as ex:
            error_msg = "Error when converting QuickTrack api message to bytes. Error :{}".format(ex)
            DutLogger.log(LogCategory.ERROR, error_msg)
            raise Exception(error_msg)


    def write_to_log(self):
        DutLogger.log(
            LogCategory.DEBUG,
            "Message Version :" + str(self.message_version) +
            "\nMessage Type :" + self.message_type.name +
            "\nMessage ID:"+ hex(self.message_id)
        )

    def decode_bytes(self, message_bytes: bytes):
        """Method that takes in byte values returned by the DUT and extract all the QuickTrack message variables.

        Parameters
        ----------
        message_bytes : bytearray
            Bytes returned from the DUT over the control path.
        """
        try:
            if len(message_bytes) >= 7:
                self.message_version = message_bytes[0]
                self.message_type = QuickTrackMessageType(int.from_bytes(message_bytes[1:3], byteorder='big', signed=False))
                self.message_id = int.from_bytes(message_bytes[3:5], byteorder='big', signed=False)
                #Bytes 5-7 are reserved
                self.write_to_log()
                self.message_params = self.__decode_message_params(message_bytes[7:])
                DutLogger.log(LogCategory.DEBUG, "message_params :" + str(self.message_params))
            else:
                DutLogger.log(LogCategory.ERROR, "QuickTrack message must have minimum of 7 bytes, byte received {}".format(message_bytes))
        except Exception as ex:
            DutLogger.log(LogCategory.ERROR, "Error when decoding QuickTrack api message from bytes. Error :{}\n".format(ex))

    def __decode_message_params(self, tlv_bytes: bytes):
        """Method that extracts all the message_params that are present in the response from the DUT.

        Parameters
        ----------
        tlv_bytes : bytearray
            Bytes returned from the DUT over the control path.

        Returns
        -------
        tlv_dict : dict
            Dictionary containing all the message_params that are sent from the DUT.
        """
        tlv_dict = {}
        i = 0

        while i < len(tlv_bytes):
            tlv_type = int.from_bytes(tlv_bytes[i:i+2], byteorder='big', signed=False)
            enum_type = self.__get_enum_from_byte(tlv_type)
            length = tlv_bytes[i + 2]
            next_tlv_start = i + 3 + length
            tlv_value_start_index = i + 3

            if enum_type is not None:
                if enum_type in tlv_dict:
                    tlv_values = []
                    tlv_values.append(tlv_dict[enum_type])
                    tlv_values.append(
                        tlv_bytes[tlv_value_start_index:next_tlv_start]
                        .decode("utf-8")
                        .lstrip("\x00")
                    )
                    tlv_dict[enum_type] = tlv_values
                else:
                    tlv_dict[enum_type] = (
                        tlv_bytes[tlv_value_start_index:next_tlv_start]
                        .decode("utf-8")
                        .lstrip("\x00")
                    )

            i = next_tlv_start
        return tlv_dict

    def __get_enum_from_byte(self, tlv_type: int):
        """Utility method to get the type of TLV using its byte value.

        Parameters
        ----------
        tlv_type : int
            Raw byte value for the TLV

        Returns
        -------
        Enum
            The corresponding enum representing the TLV based on its byte value.
        """
        try:
            if self.message_type == QuickTrackMessageType.CMD_RESPONSE or self.message_type == QuickTrackMessageType.CMD_ACK:
                return QuickTrackResponseTLV(tlv_type)
            else:
                return QuickTrackRequestTLV(tlv_type)
        except Exception as ex:
            error_msg = "Error when decoding TLV type. Error :{}".format(ex)
            DutLogger.log(LogCategory.ERROR, error_msg)
            raise Exception(error_msg)

    def __get_tlv_byte_array(self, tlv_type : int, tlv_value : str):
        """Helper method for adding the Tlvs to the command_raw_data.

        Parameters
        ---------
        tlv_type : int
            Type of TLV
        tlv_value :
            Value of TLV
        Returns
        -------
        array
            TLV byte array

        """
        tlv_type_bytes = tlv_type.to_bytes(2,byteorder='big')
        tlv_value_bytes = bytearray(tlv_value.encode())

        single_tlv_data = []
        single_tlv_data.extend(tlv_type_bytes)
        single_tlv_data.append(len(tlv_value_bytes))
        single_tlv_data.extend(tlv_value_bytes)
        return single_tlv_data
