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
import getopt
import sys
import re
from Commands.command import ApiReturnStatus, ApiInterface, Command
from typing import Type
from Commands.dut_logger import DutLogger, LogCategory
try:
    from Commands.XXX_command_helper import XXX_CommandHelper as CommandHelper
except ImportError:
    from Commands.command_helper import CommandHelper
from Commands.shared_enums import BssIdentifierBand


IP_REGEX = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
ETHERNET_PORT_REGEX = r"^([0-5])?(?(1)\d{1,4}$|^\d{1,4}$)|^[0-6]{3}[0-3][0-5]$"
DEFAULT_PORT = "9004"
DEFAULT_BAUDRATE = "57600"


class ControlAppHelper:
    @staticmethod
    def execute_control_app_api(api_to_execute: Type[ApiInterface]) -> ApiReturnStatus:
        """Method to execute the specific QuickTrack API command implementation for the DUT

        Parameters
        ----------
        api_to_execute : Type[ApiInterface]
            Type of API to execute

        """
        api_to_execute.execute()
        ret_val = api_to_execute.get_return_status()
        return ret_val

    # Obsolete
    @staticmethod
    def get_interface_names(prefix_name):
        """Method to scan all interface names with prefix_name
        """ 
        
        interface_names = command_interpreter_obj.execute_array(
            Command.GET_INTERFACE_NAME.value, [prefix_name]
        )
        DutLogger.log(LogCategory.INFO, f"\nScanned interface names are : {interface_names}\n")
        return interface_names


    @staticmethod
    def get_default_wlan_name():
        """Gets all wireless interface names, provide option for user to
        select interface name manually

        Returns
        -------
        str
            name of the using wireless interface
        """
        interface_names = CommandHelper.get_all_wlan_name()
        if len(interface_names) == 0:
            interface = input(
                "\nApp did not detect any interfaces, please enter the name of the interface to be used :\t"
            )
        elif len(interface_names) > 1:
            interface = ControlAppHelper.__get_interface_from_available_options(interface_names)
        else:
            interface = interface_names[0]
        DutLogger.log(LogCategory.INFO, f"Configuring {interface} as interface for control app usage.\n")
        return interface

    @staticmethod
    def set_wireless_if(name_arg):
        if name_arg.find(":") == -1:
            CommandHelper.INTERFACE_LOGICAL_NAME = name_arg
        else:
            band_name = name_arg.split(",")
            for x in band_name:
                if x[0:2] == "2:":
                    name_list = [BssIdentifierBand._24GHz.value, x[2:], 0]
                if x[0:2] == "5:":
                    name_list = [BssIdentifierBand._5GHz.value, x[2:], 0]
                if x[0:2] == "6:":
                    name_list = [BssIdentifierBand._6GHz.value, x[2:], 0]
                std_out, std_err = CommandHelper.check_wlan_created(x[2:])
                if not std_out: # Create if not exist
                    CommandHelper.create_wlan_if(x[2:])
                CommandHelper.INTERFACE_LIST.append(name_list)

    @staticmethod
    def __get_interface_from_available_options(interface_names):
        """Gets the interface name from user among available options

        Parameters
        ----------
        interface_names : list
            list of interface names detected

        Returns
        -------
        str
            interface name chosen by the user
        """
        DutLogger.log(LogCategory.INFO, "interfaces detected :")
        for each_interface_name in interface_names:
            DutLogger.log(LogCategory.INFO, each_interface_name)
        count = 5
        while count > 0:
            interface = input("\nEnter the name of the interface to be used :\t")
            if interface in interface_names:
                break
            else:
                exit_status = input(
                    "\nEnter 'E/e' to exit, any other key to continue: "
                ).upper()
                if exit_status == "E":
                    exit()
            count -= 1
        return interface

    @staticmethod
    def get_optional_parameters():
        """Gets the optional parameters from the app run

        Returns
        -------
        dict
            dictionary containing parameter and its value
        """
        try:
            argv = sys.argv[1:]
            options, args = getopt.getopt(argv,"",["interface=", "ip=", "port="])
            return dict(options)
        except getopt.GetoptError as err:
            DutLogger.log(LogCategory.ERROR, "Error in fetching optional parameters :" + str(err))
            exit()

    @staticmethod
    def get_ethernet_connection_inputs(options):
        """Gets the inputs for DUT ethernet connection from given options

        Parameters
        ----------
        options : dict
            dictionary of optional parameters

        Returns
        -------
        str
            ethernet IP address and port
        """
        ethernet_ip = ControlAppHelper.__get_ethernet_ip(options)
        if "--port" in options.keys():
            arg = options.get("--port")
            regex_ip_port = re.search(ETHERNET_PORT_REGEX, arg)
            if regex_ip_port is not None:
                ethernet_port = arg
                return ethernet_ip, ethernet_port
            else:
                DutLogger.log(LogCategory.ERROR, "Invalid port number given, hence using default port " + DEFAULT_PORT + "\n")
        else:
            DutLogger.log(LogCategory.INFO, "Port number not provided, hence using default port " + DEFAULT_PORT + "\n")
        ethernet_port = DEFAULT_PORT
        return ethernet_ip, ethernet_port

    @staticmethod
    def __get_ethernet_ip(options):
        """Gets valid ethernet IP address from user input, if not present returns default ip

        Parameters
        ----------
        options : dict
            dictionary of optional parameters

        Returns
        -------
        str
            ethernet IP address
        """
        if "--ip" in options.keys():
            arg = options.get("--ip")
            regex_ip = re.search(IP_REGEX, arg)
            if regex_ip is not None:
                return arg
            else:
                DutLogger.log(LogCategory.ERROR, "Invalid IP address, hence configuring default IP\n")
        else:
            DutLogger.log(LogCategory.INFO, "IP address not specified, hence using INADDR_ANY\n")
            return "0.0.0.0"
