#!/usr/bin/env python3
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

from interfaces.connection_info import ConnectionInfo, ConnectionType
from interfaces.ethernet_control_path import EthernetControlPath
#from interfaces.uart_control_path import UartControlPath
from parsers.quicktrack_api_parser import QuickTrackApiParser
from api.quicktrack_api_linux import QuickTrackApiLinux
from api.control_app_helper import ControlAppHelper
try:
    from Commands.XXX_command_helper import XXX_CommandHelper as CommandHelper
except ImportError:
    from Commands.command_helper import CommandHelper
from Commands.dut_logger import DutLogger, LogCategory
from datetime import datetime

class dutControlApp:
    interface_name = None

    def __init__(self, connection_info):
        """
        Configures the dut control app and initialized the
        required type of server
        """
        now = datetime.now()
        dt_string = now.isoformat()
        DutLogger.log_file_name = "dut_control_app_logs_{}.log".format(dt_string)
        self.connection_info = connection_info
        api_impl = QuickTrackApiLinux()
        self.api_parser = QuickTrackApiParser(api_impl)
        if self.connection_info.connection_type == ConnectionType.ETHERNET:
            self.server = EthernetControlPath(
                connection_info.ip_address, connection_info.ip_port, self.api_parser
            )

if __name__ == "__main__":
    CommandHelper.check_if_root_user()

    options = ControlAppHelper.get_optional_parameters()
    if options.get("--interface") is None:
        CommandHelper.INTERFACE_LOGICAL_NAME = ControlAppHelper.get_default_wlan_name()
    else:
        ControlAppHelper.set_wireless_if(options.get("--interface"))
        DutLogger.log(LogCategory.INFO, "Configuring {} as interface for control app usage.\n".format(CommandHelper.get_interface_name()))

    # Use Ethernet as control interface
    ethernet_ip, ethernet_port = ControlAppHelper.get_ethernet_connection_inputs(options)
    dut_control_app_obj = dutControlApp(
        ConnectionInfo(ConnectionType.ETHERNET, ip_address=ethernet_ip, ip_port=ethernet_port)
    )
    dut_control_app_obj.server.start()
