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
"""Utility module used in api commands."""
import subprocess
import os
from pathlib import Path
from .shared_enums import *
import fcntl
import socket
import struct

write_commands_into_file = False
# Set this flag to True if command and its output should be logged in a debug file
current_path = Path(os.path.realpath(""))
debug_file_path = (
    current_path / "QuickTrack-Tool/Test-Services/command_execution_debug_file.txt"
)
from time import sleep
from Commands.dut_logger import DutLogger, LogCategory
from .command import Command
from .command_interpreter import CommandInterpreter

command_interpreter_obj = CommandInterpreter()

class CommandHelper:
    """Class that contains all the utility methods for processing api commands."""

    INTERFACE_LOGICAL_NAME = None
    STATIC_IP = None
    INTERFACE_LIST = []
    BSSID_COUNT = 0
    BRIDGE_WLANS = "br-wlans"
    DHCP_SERVER_IP = "192.168.65.1"

    @staticmethod
    def add_tlvs(command_type, command_data):
        """Helper method for adding the TLV's(type-length-value) to the command_raw_data.

        Parameters
        ----------
        command_type : [byte]
            [Type of Command]
        command_data : [byte_array]
            [Commands value ]

        """
        single_tlv_data = []
        single_tlv_data.append(command_type)
        single_tlv_data.append(len(command_data))
        single_tlv_data.extend(command_data)
        return single_tlv_data

    @staticmethod
    def run_shell_command(shell_command: str, new_terminal=False):
        """Executes the specified command on a linux shell.

        Parameters
        ----------
        shell_command : str
            [shell command to be executed]

        """
        DutLogger.log(LogCategory.DEBUG, "Executing command: " + shell_command)
        if new_terminal:
            os.system("gnome-terminal -- /bin/bash -c '" + shell_command + "'")
            CommandHelper.__write_commands_into_debug_file(shell_command, "")
        else:
            output = subprocess.Popen(
                shell_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            std_out, std_err = output.communicate()
            if type(std_out) is bytes:
                std_out = std_out.decode("utf-8")

            if std_out is not None:
                DutLogger.log(LogCategory.DEBUG, "Command output: " + std_out)
                CommandHelper.__write_commands_into_debug_file(shell_command, std_out)
            if std_err is not None:
                DutLogger.log(LogCategory.ERROR, "Command output: " + std_err)
                CommandHelper.__write_commands_into_debug_file(shell_command, std_err)
            return std_out, std_err

    @staticmethod
    def __write_commands_into_debug_file(shell_command: str, command_output: str):
        """Writes the shell command and its output into file for Debug purpose.

        Parameters
        ----------
        shell_command : str
            Command that is being executed.
        command_output : str
            Output of the command being executed.
        """
        if write_commands_into_file is True:
            try:
                file_obj = open(debug_file_path, "a")
                file_obj.write("###################\nCOMMAND: " + shell_command)
                file_obj.write("\n" + command_output)
            except Exception:
                pass

    @staticmethod
    def pause_execution(time: int):
        """Utility method for sleep/wait

        Parameters
        ----------
        time : [int]
            [sleep time specified in seconds.]
        """
        DutLogger.log(LogCategory.INFO, ("Execution paused for {} seconds").format(time))
        sleep(time)

    @staticmethod
    def check_if_root_user():
        """checks if the app is run as root user
        """
        if CommandHelper.run_shell_command("whoami")[0].strip() != "root":
            DutLogger.log(LogCategory.ERROR, "Please restart the DUT control app with root permission to continue\n")
            exit()

    @staticmethod
    def check_wlan_created(if_name):
        return CommandHelper.run_shell_command("iw dev | grep {}".format(if_name))

    @staticmethod
    def create_wlan_if(if_name):
        CommandHelper.run_shell_command(
            "iw phy phy0 interface add {} type managed".format(if_name)
        )

        # Make sure MAC address is unique
        std_out, std_err = CommandHelper.run_shell_command("iw dev | grep addr")
        addr_list = std_out.split("\n")
        if len(addr_list) == len(set(addr_list)):
            return
        # MAC addr is the same and need to change
        new_interface_mac = CommandHelper.get_hw_addr(if_name).split(':')
        changed = int(new_interface_mac[5], base=16) + 4
        new_interface_mac[5] = format(changed, 'x')
        new_interface_mac = ":".join(new_interface_mac)
        CommandHelper.run_shell_command(
            "sudo ip link set dev {} address {}".format(
            if_name, new_interface_mac)
        )

    @staticmethod
    def get_hw_addr(ifname):
        # https://stackoverflow.com/questions/159137/getting-mac-address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
        return ':'.join('%02x' % b for b in info[18:24])

    @staticmethod
    def create_new_interface_bridge_network():
        """Returns the new interface bridge network."""
        std_out, std_err = CommandHelper.run_shell_command("sudo brctl -V")
        if std_err is None:
            CommandHelper.run_shell_command("sudo brctl addbr {}".format(CommandHelper.BRIDGE_WLANS))

            CommandHelper.run_shell_command("sudo ip link set {} up".format(CommandHelper.BRIDGE_WLANS))

        return std_out, std_err

    @staticmethod
    def add_all_interfaces_to_bridge():
        """Creates a bridge network with the existing wireless interface and the
        wireless interface name sent from the tool
        """
        for if_info in CommandHelper.INTERFACE_LIST:
            if if_info[2] > 0:
                CommandHelper.run_shell_command(
                    ("sudo brctl addif {} {}").format(CommandHelper.BRIDGE_WLANS, if_info[1])
                )   

    @staticmethod
    def get_all_interface_ip():
        return CommandHelper.run_shell_command("sudo ip addr")

    @staticmethod
    def reset_bridge_network():
        """Clears all the bridge network if any and will reassign the ip that was
        assigned to the wireless interface before bridge was created
        """
        std_out, std_err = CommandHelper.get_all_interface_ip()
        if CommandHelper.BRIDGE_WLANS in std_out:
            CommandHelper.run_shell_command("sudo ip link set {} down".format(CommandHelper.BRIDGE_WLANS))
            CommandHelper.run_shell_command(
                "sudo timeout -k 5 10 brctl delbr {}".format(CommandHelper.BRIDGE_WLANS)
            )

    @staticmethod
    def reset_interface_ip(if_name):
        CommandHelper.run_shell_command("sudo ip addr flush dev {}".format(if_name))

    @staticmethod
    def assign_static_ip(dut_static_ip, input_interface_name=None):
        """Assigns the static IP for the DUT."""
        CommandHelper.STATIC_IP = dut_static_ip

        std_out, std_err = CommandHelper.get_all_interface_ip()
        if CommandHelper.BRIDGE_WLANS in std_out:#If bridge network present assign ip to it.
            CommandHelper.run_shell_command("sudo ip addr add {}/24 dev {}".format(dut_static_ip, CommandHelper.BRIDGE_WLANS))
            return True

        if input_interface_name:
            interface_name = input_interface_name
        else:
            interface_name = CommandHelper.get_interface_name()
        if interface_name:
            CommandHelper.run_shell_command("sudo ip addr flush dev {}".format(interface_name))
            CommandHelper.run_shell_command(
                ("sudo ip addr add {}/24 dev {}").format(
                    dut_static_ip, interface_name
                )
            )
            return True
        else:
            return False

    @staticmethod
    def clear_bss_identifiers():
        # Reset bss_id in interface list
        for x in CommandHelper.INTERFACE_LIST:
            x[2] = 0
        CommandHelper.BSSID_COUNT = 0
        # Todo: Need to create not first WLAN again as hostapd will remove bss in appending conf case

    @staticmethod
    def set_interface_bss_id(band, bss_id):
        if CommandHelper.INTERFACE_LIST:
            for if_info in CommandHelper.INTERFACE_LIST:
                if if_info[0] == band and if_info[2] == 0:
                    if_info[2] = bss_id
                    CommandHelper.BSSID_COUNT += 1
                    return if_info[1]
        DutLogger.log(LogCategory.INFO, "Can't set bss id to available interface based on band, Please check --interface argument")
        DutLogger.log(LogCategory.INFO, "use default wireless interface")
        return CommandHelper.INTERFACE_LOGICAL_NAME

    @staticmethod
    def get_interface_name(bss_id = None):
        if bss_id is not None:
            for if_info in CommandHelper.INTERFACE_LIST:
                if if_info[2] == bss_id:
                    return if_info[1]
            return None
        if CommandHelper.INTERFACE_LOGICAL_NAME: 
            return CommandHelper.INTERFACE_LOGICAL_NAME
        elif CommandHelper.INTERFACE_LIST:
            for if_info in CommandHelper.INTERFACE_LIST:
                if if_info[2] > 0:
                    return if_info[1]
            return CommandHelper.INTERFACE_LIST[0][1]
        DutLogger.log(LogCategory.ERROR, "Can't get any valid interface, Please check --interface argument")
        return None

    # Return the list of all wireless interface name
    @staticmethod
    def get_all_wlan_name():
        return command_interpreter_obj.execute_array(
            Command.GET_INTERFACE_NAME.value, ["wl"]
        )

    @staticmethod
    def get_if_ip_addr(if_name):
        return command_interpreter_obj.execute(
            Command.GET_INTERFACE_IP_ADD.value, [if_name]
        )

    @staticmethod
    def get_if_mac_addr(if_name):
        return command_interpreter_obj.execute(
            Command.GET_MAC_ADDR.value, [if_name]
        )

    @staticmethod
    def verify_band_from_freq(freq: str, band: str):
        """Utility method to return the operational band based on the frequency.
        Parameters
        ----------
        freq : str
            Frequency value to be verified if present in required band.
        band : OperationalBand
            Band value to be verified with
        """
        current_op_band = None
        _, _24G_frequencies = ChannelFreqConfig.get_24G_channels_frequencies()
        _, _5G_frequencies = ChannelFreqConfig.get_5G_channels_frequencies()
        if freq in _24G_frequencies:
            current_op_band = OperationalBand._24GHz.name
        elif freq in _5G_frequencies:
            current_op_band = OperationalBand._5GHz.name

        if current_op_band == band:
            return True
        else:
            return False

    # Return addr of P2P-device if there is no GO or client interface
    @staticmethod
    def get_p2p_mac_addr():
        mac = None

        std_out, std_err = CommandHelper.run_shell_command("iw dev")        
        line_list = std_out.splitlines()
        for line in line_list:
            if line.find("addr") != -1:
                addr = line.split()
            if line.find("type") != -1:
                dev_type = line.split()
                if dev_type[1] == "P2P-GO" or dev_type[1] == "P2P-client":
                    return addr[1]
                elif dev_type[1] == "P2P-device":
                    mac = addr[1]
        
        return mac

    @staticmethod
    def get_p2p_group_interface():
        std_out, std_err = CommandHelper.run_shell_command("iw dev")        
        line_list = std_out.splitlines()
        for line in line_list:
            if line.find("Interface") != -1:
                if_name = line.split()
            if line.find("type") != -1:
                dev_type = line.split()
                if dev_type[1] == "P2P-GO" or dev_type[1] == "P2P-client":
                    return if_name[1]

        DutLogger.log(LogCategory.INFO, "Can't get P2P Group Interface")
        return None

    @staticmethod
    def get_p2p_dev_interface():
        p2p_dev = "p2p-dev-{}".format(CommandHelper.INTERFACE_LOGICAL_NAME)
        return p2p_dev

    @staticmethod
    def start_dhcp_server(if_name, ip_addr):
        offset = ip_addr.rfind(".")
        ip_sub = ip_addr[0:offset]
        CommandHelper.run_shell_command("cp QT_dhcpd.conf /etc/dhcp/QT_dhcpd.conf")
        f = open("/etc/dhcp/QT_dhcpd.conf", "a")
        cmd = "\nsubnet {}.0 netmask 255.255.255.0".format(ip_sub)
        cmd += " {\n"
        f.write(cmd)
        cmd = "    range {}.50 {}.200;\n".format(ip_sub, ip_sub)
        f.write(cmd)
        f.write("}\n")
        f.close()
        CommandHelper.run_shell_command("touch /var/lib/dhcp/dhcpd.leases_QT")
        cmd = "dhcpd -4 -cf /etc/dhcp/QT_dhcpd.conf -lf /var/lib/dhcp/dhcpd.leases_QT {}".format(if_name)
        CommandHelper.run_shell_command(cmd)

    @staticmethod
    def start_dhcp_client(if_name):
        cmd = "dhclient -4 {} &".format(if_name)
        CommandHelper.run_shell_command(cmd)

    @staticmethod
    def stop_dhcp_server():
        CommandHelper.run_shell_command("killall dhcpd 1>/dev/null 2>/dev/null")

    @staticmethod
    def stop_dhcp_client():
        CommandHelper.run_shell_command("killall dhclient 1>/dev/null 2>/dev/null")
    
    @staticmethod
    def get_process_id(name):
        return CommandHelper.run_shell_command("sudo pidof {}".format(name))

    @staticmethod
    def get_wps_settings(role):
        wps_config = []
        if role == WpsDeviceRole.WPS_AP:
            if os.path.exists("/tmp/wsc_settings_APUT"):
                with open("/tmp/wsc_settings_APUT", "r") as file:
                    for line in file:
                        config_list = line.split(":")
                        wps_config.append(config_list)
            else:
                DutLogger.log(LogCategory.ERROR, "APUT: WPS Erorr. Failed to get settings.")
        else:
            if os.path.exists("/tmp/wsc_settings_STAUT"):
                with open("/tmp/wsc_settings_STAUT", "r") as file:
                    for line in file:
                        config_list = line.split(":")
                        wps_config.append(config_list)
            else:
                DutLogger.log(LogCategory.ERROR, "STAUT: WPS Erorr. Failed to get settings.")
        return wps_config

