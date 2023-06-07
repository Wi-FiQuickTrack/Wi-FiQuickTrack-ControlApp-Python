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
from enum import Enum


class ConnectionInfo:  # noqa : D100
    """
    Class that provide info on the dut control path.

    The class provides details about the type of control path being used and
    provides the required address/port details for setting up the control app
    server on the dut.
    """

    def __init__(
        self, connection_type, ip_address="", ip_port="", uart_port="", baud_rate=""
    ):
        """Type of physical connetion being used."""
        self.connection_type = connection_type
        """IP address details in case of ethernet based connection"""
        self.ip_address = ip_address
        self.ip_port = ip_port


class ConnectionType(Enum):
    """Enum Class which gives the connection type."""

    ETHERNET = (1,)
