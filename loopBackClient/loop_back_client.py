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
from threading import Thread
from time import sleep
from Commands.dut_logger import DutLogger, LogCategory

class LoopBackClient:
    """
    Simple UDP socket for loop back data.

    implementation that echos back any loop back test data sent for the
    test tool.
    """

    def __init__(self, local_address, local_port):
        try:
            self.local_address = local_address
            self.local_port = int(local_port)
            self.loop_back_app_closed = False
            self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client.bind((self.local_address, self.local_port))
            self.client.settimeout(30.0)

            if self.local_port == 0:
                self.local_port = self.client.getsockname()[1]
                DutLogger.log(LogCategory.INFO, "Loopback server port is {}".format(self.local_port))

            listening_thread = Thread(target=self.start_listening)
            listening_thread.setDaemon(True)
            listening_thread.start()
        except Exception as ex:
            DutLogger.log(LogCategory.ERROR, "Error when starting loop back server :" + str(ex))
            return None

    def start_listening(self):
        """Starts the loop back client on the specified port number and echos back any data received from the test tool
        """
        try:
            # connect to the server
            DutLogger.log(
                LogCategory.INFO,
                "Start loop back server at -"
                + self.local_address
                + ":"
                + str(self.local_port)
            )

            while self.loop_back_app_closed is False:
                # receive data stream. it won't accept data packet greater
                #  than 1024 bytes
                try:
                    data, addr = self.client.recvfrom(1400)
                    if data:
                        DutLogger.log(LogCategory.DEBUG, "Received data from test tool :" + str(addr))
                        self.client.sendto(data, addr)
                    sleep(0.1)
                except Exception:
                    pass  # Expected to timeout

        except Exception as ex:
            DutLogger.log(LogCategory.ERROR, "Error when connecting with QuickTrack tool :" + str(ex))
            return None

    def get_port(self):
        return self.local_port

    def close(self):
        """Shuts the UDP loopback app
        """
        self.loop_back_app_closed = True
        sleep(0.5)
        self.client.close()
