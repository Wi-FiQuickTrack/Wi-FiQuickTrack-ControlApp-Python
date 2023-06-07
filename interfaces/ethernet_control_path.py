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
import socket
import sys
from interfaces.control_path import ControlPath
import json
from time import sleep
from Commands.command import ApiReturnStatus
from quicktrack_api_message.quicktrack_api_message import QuickTrackAPIMessage, QuickTrackMessageType
from Commands.dut_logger import DutLogger, LogCategory

class EthernetControlPath(ControlPath):
    """
    Sample implemtation for ethernet based control path.
    """

    def __init__(self, local_address, local_port, quicktrack_api_parser):
        self.host = local_address
        self.port = int(local_port)
        self.addr_port = (self.host, self.port)
        self.quicktrack_api_parser = quicktrack_api_parser

    def start(self):
        """Starts a tcp socket server to receive all the api in tlv format
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.client.bind((self.host, self.port))
        except Exception as err:
            DutLogger.log(LogCategory.ERROR, err)

        DutLogger.log(LogCategory.INFO, "QuickTrack control app running at  : " + self.host + ":" + str(self.port))
        while True:
            # receive data stream. it won't accept data packet greater
            #  than 1024 bytes
            try:
                data, self.address = self.client.recvfrom(1024)
            except Exception as err:
                DutLogger.log(LogCategory.ERROR, err)
            if data:
                received_message = self.quicktrack_api_parser.decode(data)
                acknowledgement = ApiReturnStatus(0, str("ACK: Command received"))
                if (received_message.message_type is None):
                    acknowledgement = ApiReturnStatus(1, str("NACK: Error in received QuickTrack API message"))

                message_tlv = acknowledgement.to_dict()
                acknowledgement_message = QuickTrackAPIMessage(QuickTrackMessageType.CMD_ACK, message_tlv)
                acknowledgement_message.set_message_id(received_message.message_id)
                self.client.sendto(acknowledgement_message.get_message_bytes(), self.address)

                if received_message.message_params is None:
                    execution_result = ApiReturnStatus(1, "Wrong/Unkown Request TLV")
                else:
                    execution_result = self.quicktrack_api_parser.execute(received_message)
                message_tlv = execution_result.to_dict()
                response_message = QuickTrackAPIMessage(QuickTrackMessageType.CMD_RESPONSE, message_tlv)
                response_message.set_message_id(received_message.message_id)
                self.client.sendto(response_message.get_message_bytes(), self.address)
                sleep(0.1)

    def sendToClient(self, data):
        """Sends back the api output

        Arguments:
            data  -- Output data to be sent to the client
        """
        self.client.sendto(data, self.addr_port)

    def stop(self):
        """Closes the control app
        """
        self.client.close()  # close the connection
