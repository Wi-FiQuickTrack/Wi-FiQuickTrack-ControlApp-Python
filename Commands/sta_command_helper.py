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
try:
    from .XXX_command_helper import XXX_CommandHelper as CommandHelper
except ImportError:
    from .command_helper import CommandHelper
from .shared_enums import DebugLogLevel, P2PConnType, WpsDeviceRole
from .command_interpreter import CommandInterpreter
from .command import Command
import os
from datetime import datetime
from Commands.dut_logger import DutLogger, LogCategory
from datetime import datetime

command_interpreter_obj = CommandInterpreter()
store_wpas_config_for_debug = False
sta_debug_log_level = DebugLogLevel.DISABLE
wpa_supplicant_log_folder_path = "/var/log/supplicant.log"
wpa_supplicant_config_file = "/etc/wpa_supplicant/wpa_supplicant.conf"
# Default DUT GO intent value
P2P_GO_INTENT = 7

wpa_config_header = (
    "sta_sae_groups", "mbo_cell_capa", "sae_pwe",
    "update_config",
)

def get_server_cert_hash(pem_file):
    # These were generated with: openssl x509 -outform der -in $pemname | openssl dgst -sha256
    entries = {
        "rsa_server1_w1_fi.pem": "a7407d995678712bb7adb4e7a75e89674aba363dea0b8308c63b006329b0de2d",
        "rsa_server1ALT_w1_fi.pem": "79a9d7273368bee41566f79ae9fc84119f7c963cf8cfac5984e2e0adaeafb112",
        "rsa_server2_w1_fi.pem": "8d0e00b924e30f4595ae7f5ef9f1346e2c3f343dfb1caf1429b3bb6b32a1bf03",
        "rsa_server4_w1_fi.pem": "2703264d2d06727be661752ff5b57e85f842dc74e18aaa03316e7b2d08db6260",
    }
    return "hash://server/sha256/{}".format(entries[pem_file])

class StaCommandHelper:
    store_test_artifcats = False

    @staticmethod
    def get_wpa_supp_config(config_enums: dict, merge_config_file: bool) -> str:  # noqa:E999
        """Method to get the wpa supplicant configuration.
        Parameters
        ----------
        config_enums: dict
            Configurations in TLVs
        merge_config_file : bool
            Flag to indicate if new supplicant config file has to be create or the new config has to be merged into existing file

        Returns
        -------
        WPA Configuration"""

        wpa_supplicant_config = "ctrl_interface=/var/run/wpa_supplicant\nap_scan=1\npmf=1\n"

        for each_config_enum in config_enums:
            if each_config_enum in wpa_config_header:
                field_value = config_enums.get(each_config_enum)
                if each_config_enum == "sta_sae_groups":
                    wpa_supplicant_config += "sae_groups" + "=" + field_value + "\n"
                else:
                    wpa_supplicant_config += each_config_enum + "=" + field_value + "\n"

        wpa_supplicant_config += "network={\n"
        wpa_supplicant_config_mapper = {
            "sta_ssid": True,
            "key_mgmt": False,
            "sta_wep_key0": False,
            "wep_tx_keyidx": False,
            "group": False,
            "psk": True,
            "proto": False,
            "sta_ieee80211w": False,
            "pairwise": False,
            "eap": False,
            "phase2": True,
            "phase1": True,
            "identity": True,
            "password": True,
            "ca_cert": True,
            "server_cert": True,
            "private_key": True,
            "client_cert": True,
            "domain_match": True,
            "domain_suffix_match": True,
            "pac_file": True,
            "sta_owe_group": False,
        }
        ieee80211w_configured = False
        transition_mode_enabled = False
        owe_configured = False
        sae_configured = False
        for each_config_enum in config_enums:
            if each_config_enum and each_config_enum not in wpa_config_header:
                quoted_string = wpa_supplicant_config_mapper.get(each_config_enum)
                field_value = config_enums[each_config_enum]

                if each_config_enum == "key_mgmt":
                    if "WPA-PSK" in field_value and "SAE" in field_value:
                        transition_mode_enabled = True
                    if "OWE" in field_value:
                        owe_configured = True
                    if "SAE" in field_value:
                        sae_configured = True
                elif each_config_enum == "sta_ieee80211w":
                    ieee80211w_configured = True

                if each_config_enum == "ca_cert":
                    if "DEFAULT" in field_value:
                        field_value = '/etc/ssl/certs/ca-certificates.crt'

                if each_config_enum == "server_cert":
                    field_value = get_server_cert_hash(field_value)

                if quoted_string:
                    field_value = '"' + field_value + '"'
                # Mapping to correct wpa_supplicant config name
                if each_config_enum == "sta_ssid":
                    wpa_supplicant_config += "ssid" + "=" + field_value + "\n"
                elif each_config_enum == "sta_wep_key0":
                    wpa_supplicant_config += "wep_key0" + "=" + field_value + "\n"
                elif each_config_enum == "server_cert":
                    wpa_supplicant_config += "ca_cert" + "=" + field_value + "\n"
                elif each_config_enum == "sta_owe_group":
                    wpa_supplicant_config += "owe_group" + "=" + field_value + "\n"
                elif each_config_enum == "sta_ieee80211w":
                    wpa_supplicant_config += "ieee80211w" + "=" + field_value + "\n"
                else:
                    wpa_supplicant_config += each_config_enum + "=" + field_value + "\n"

        if not ieee80211w_configured:
            if transition_mode_enabled:
                wpa_supplicant_config += "ieee80211w=1\n"
            elif owe_configured:
                wpa_supplicant_config += "ieee80211w=2\n"
            elif sae_configured:
                wpa_supplicant_config += "ieee80211w=2\n"

        if merge_config_file:
            appended_supplicant_conf_str = ""
            existing_conf = StaCommandHelper.get_existing_supplicant_conf()
            wpa_supplicant_dict = StaCommandHelper.__convert_config_str_to_dict(config = wpa_supplicant_config)
            for each_key in existing_conf:
                if each_key not in wpa_supplicant_dict:
                    wpa_supplicant_dict[each_key] = existing_conf[each_key]

            for each_supplicant_conf in wpa_supplicant_dict:
                appended_supplicant_conf_str += each_supplicant_conf + "=" + wpa_supplicant_dict[each_supplicant_conf] + "\n"
            wpa_supplicant_config = appended_supplicant_conf_str.rstrip()
        wpa_supplicant_config += "\n}"
        return wpa_supplicant_config

    @staticmethod
    def get_existing_supplicant_conf():
        """Returns the existing supplicant configuration that was previously configured."""
        existing_config = {}
        if os.path.exists(wpa_supplicant_config_file):
            with open(wpa_supplicant_config_file, "r") as file_reader:
                lines_to_ignore = ["ap_scan", "network", "ctrl_interface"]
                for each_line in file_reader:
                    if "=" in each_line and not any(x in each_line for x in lines_to_ignore):
                        key, val = each_line.split("=", 1)
                        existing_config[key] = val.rstrip()
        return existing_config

    @staticmethod
    def store_supplicant_config():
        """Stores the existing supplicant configuration in /var/log folder"""
        now = datetime.now()
        dt_string = now.isoformat()
        if os.path.exists(wpa_supplicant_config_file):
            quicktrack_configs_folder = "/var/log/quicktrack_configs/"
            if not os.path.exists(quicktrack_configs_folder):
                CommandHelper.run_shell_command("sudo mkdir {}".format(quicktrack_configs_folder))
            CommandHelper.run_shell_command("sudo mv {} {}wpa_supplicant_{}.conf".format(wpa_supplicant_config_file, quicktrack_configs_folder, dt_string))

    @staticmethod
    def __convert_config_str_to_dict(config:str):
        """Converting string into dictionary using dict comprehension

        Parameters
        ----------
        config : [dict]
            Converts the configuration from datatype string to dictionary.
        """
        config_temp_list = []
        config_list = [each_config.split("=", 1) for each_config in config.split("\n")]
        for each_config in config_list:
            for each_key in each_config:
                config_temp_list.append(each_key)
        config_dict = dict(zip(*[iter(config_temp_list)]*2))
        return config_dict

    @staticmethod
    def sta_configure(params: dict):
        """Method to configure the wpa supplicant.

        Parameters
        ----------
        params : [dict]
            [parameters for sta wpa_supplicant configuration.]

        merge_config_file : bool
            Flag to indicate if new supplicant config file has to be create or the new config has to be merged into existing file
        """
        wpa_supplicant_config = StaCommandHelper.get_wpa_supp_config(params, False)

        try:
            with open(wpa_supplicant_config_file, "w+") as file:
                file.write(wpa_supplicant_config)
            if store_wpas_config_for_debug:
                StaCommandHelper.__store_supplicant_config_for_debug(params)
            return "Wpa supplicant successfully configured.", None
        except Exception as ex:
            return None, "Unable to configure wpa supplicant " + str(ex)


    @staticmethod
    def __store_supplicant_config_for_debug(wpa_supplicant_config):
        "Method to store the wpa supplicant config file for debug purpose."
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H:%M:%S")
        wpa_supplicant_files_path = "/etc/wpa_supplicant/wpa_supplicant_files"
        if not os.path.exists(wpa_supplicant_files_path):
            os.mkdir(wpa_supplicant_files_path)
        try:
            with open(
                "/etc/wpa_supplicant/wpa_supplicant_files/wpa_supplicant"
                + str(dt_string),
                "w+",
            ) as file:
                file.write(wpa_supplicant_config)
        except IOError as err:
            DutLogger.log(LogCategory.ERROR, "Error when creating wpa_supplicant debug file:" + str(err))

    @staticmethod
    def sta_associate():
        """Method to start the wpa_supplicant service."""
        interface_name = CommandHelper.get_interface_name()
        #StaCommandHelper.store_test_artifcats = True
        log_level = StaCommandHelper.__get_sta_debug_log_level()
        StaCommandHelper.clear_supplicant_logs()

        CommandHelper.run_shell_command("sudo rfkill unblock wlan")
        CommandHelper.run_shell_command("sudo killall wpa_supplicant")
        CommandHelper.pause_execution(3)

        supplicant_start_command = "sudo /usr/local/bin/WFA-Hostapd-Supplicant/wpa_supplicant -B -t -c {} -i {}".format(wpa_supplicant_config_file, interface_name)
        if log_level:
            supplicant_start_command += " {} -f {}".format(log_level, wpa_supplicant_log_folder_path)
        CommandHelper.run_shell_command(supplicant_start_command)

        # Skip connection check as Tool will verify
        return None

    @staticmethod
    def sta_disconnect():
        """Method to stop the wpa_supplicant service.

        Parameters
        ----------
        interface_name : [str]
            [interface name on which the supplicant needs to be stopped.]
        """
        std_out, std_err = CommandHelper.get_process_id("wpa_supplicant")
        if std_out:
            std_out, std_err = CommandHelper.run_shell_command(
                "sudo killall wpa_supplicant"
            )
            if StaCommandHelper.store_test_artifcats:
                StaCommandHelper.store_supplicant_config()
                #StaCommandHelper.__log_supplicant_logs()
                StaCommandHelper.store_test_artifcats = False
            return std_out, std_err
        else:
            return std_out, std_err

    @staticmethod
    def __log_supplicant_logs():
        global sta_debug_log_level
        if sta_debug_log_level != DebugLogLevel.DISABLE:
            if os.path.exists(wpa_supplicant_log_folder_path):
                with open(wpa_supplicant_log_folder_path, "r") as file_reader:
                    file_content = file_reader.readlines()
                if file_content:
                    DutLogger.log(LogCategory.DEBUG, "Wpa supplicant logs :" + str(file_content))
                else:
                    DutLogger.log(LogCategory.DEBUG, "Wpa supplicant debug log file is not found at {}".format(hostapd_log_folder_path))

    @staticmethod
    def __get_sta_debug_log_level():
        global sta_debug_log_level
        if sta_debug_log_level == DebugLogLevel.BASIC:
            return "-d"
        elif sta_debug_log_level == DebugLogLevel.ADVANCED:
            return "-ddd"
        else:
            return None

    @staticmethod
    def set_sta_debug_log_level(log_level):
        global sta_debug_log_level
        sta_debug_log_level = log_level

    @staticmethod
    def clear_supplicant_logs():
        """Utility method to clear supplicant debug log file stored during start associating"""
        if os.path.exists(wpa_supplicant_log_folder_path):
            CommandHelper.run_shell_command(
                "sudo rm -rf {}".format(wpa_supplicant_log_folder_path)
            )

    @staticmethod
    def start_wpa_supplicant_scan():
        global sta_debug_log_level
        interface_name = CommandHelper.get_interface_name()
        log_level = StaCommandHelper.__get_sta_debug_log_level()
        try:
            with open(wpa_supplicant_config_file, "w+") as file:
                file.write(
                    'ctrl_interface=/var/run/wpa_supplicant\nap_scan=1\nnetwork={\nssid="Scanning"\n}'
                )
        except Exception as ex:
            return None, "Unable to configure wpa supplicant and trigger scan " + str(ex)
        if log_level:
            CommandHelper.run_shell_command(
                (
                    "sudo /usr/local/bin/WFA-Hostapd-Supplicant/wpa_supplicant -B -t -c {} -i {} {} >> {}"
                ).format(wpa_supplicant_config_file, interface_name, log_level, wpa_supplicant_log_folder_path)
            )
        else:
            CommandHelper.run_shell_command("sudo /usr/local/bin/WFA-Hostapd-Supplicant/wpa_supplicant -B -t -c {} -i {} >> {}".format(wpa_supplicant_config_file, interface_name, wpa_supplicant_log_folder_path))
        CommandHelper.pause_execution(1)

        std_out, std_err = CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} scan").format(interface_name)
        )

        return std_out, std_err

    @staticmethod
    def get_sta_if_status(if_name):
        wpa_cli_status, _ = CommandHelper.run_shell_command(
            "sudo wpa_cli -i {} status".format(if_name)
        )
        interface_freq = command_interpreter_obj.apply_cmd_regex(
            Command.GET_FREQ, wpa_cli_status
        )
        interface_ssid = command_interpreter_obj.apply_cmd_regex(
            Command.GET_STA_SSID, wpa_cli_status
        )
        mac_addr = command_interpreter_obj.apply_cmd_regex(
            Command.GET_STA_DUT_MAC_ADDR, wpa_cli_status
        )
        return interface_freq, interface_ssid, mac_addr

    @staticmethod
    def start_up_p2p():
        """Method to start the wpa_supplicant service."""
        interface_name = CommandHelper.get_interface_name()
        log_level = StaCommandHelper.__get_sta_debug_log_level()
        StaCommandHelper.clear_supplicant_logs()

        CommandHelper.run_shell_command("sudo rfkill unblock wlan")
        CommandHelper.run_shell_command("sudo killall wpa_supplicant")
        CommandHelper.pause_execution(3)

        try:
            with open(wpa_supplicant_config_file, "w+") as file:
                p2p_config = "ctrl_interface=/var/run/wpa_supplicant\n"
                p2p_config += "device_name=WFA P2P Device\n"
                p2p_config += "device_type=1-0050F204-1\n"
                p2p_config += "config_methods=keypad display push_button\n"
                file.write(p2p_config)
        except Exception as ex:
            return None, "Unable to configure wpa supplicant " + str(ex)

        supplicant_start_command = "sudo /usr/local/bin/WFA-Hostapd-Supplicant/wpa_supplicant -B -t -c {} -i {}".format(wpa_supplicant_config_file, interface_name)
        if log_level:
            supplicant_start_command += " {} -f {}".format(log_level, wpa_supplicant_log_folder_path)
        CommandHelper.run_shell_command(supplicant_start_command)
        CommandHelper.pause_execution(2)

        return None
    
    @staticmethod
    def send_sta_btm_query(reason_code, cand_list):
        if_name = CommandHelper.get_interface_name()
        param_str = ""
        if reason_code != None:
            param_str += " {}".format(reason_code)
        if cand_list != None:
            if int(cand_list) == 1:
                param_str += " list"

        return command_interpreter_obj.execute(
            Command.SEND_STA_BTM_QUERY.value,
            [if_name, param_str],
        )

    @staticmethod
    def send_sta_anqp_query(bssid, id_param):
        # DUT needs to handle the supplicant for sending ANQP query during pre-association
        pid, _ = CommandHelper.get_process_id("wpa_supplicant")
        if pid:
            DutLogger.log(LogCategory.DEBUG, "wpa_supplicant is alive, pid={}".format(pid))
        else:
            DutLogger.log(LogCategory.DEBUG, "wpa_supplicant is not alive. Bring up wpa supplicant to scan")
            StaCommandHelper.start_wpa_supplicant_scan()
            CommandHelper.pause_execution(10)

        anqp_query_id_param_mapper = {
            "NeighborReportReq": "272",
            "QueryListWithCellPref": "mbo:2",
        }
        param_str = ""
        query_id_param = anqp_query_id_param_mapper.get(id_param)
        if query_id_param is not None:
            param_str += " {}".format(query_id_param)
        if_name = CommandHelper.get_interface_name()

        return command_interpreter_obj.execute(
            Command.SEND_STA_ANQP_QUERY.value,
            [if_name, bssid, param_str],
        )

    @staticmethod
    def send_sta_disconnect():
        if_name = CommandHelper.get_interface_name()

        return CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} disconnect").format(if_name)
        )

    @staticmethod
    def sta_reassociate():
        if_name = CommandHelper.get_interface_name()

        return CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} reconnect").format(if_name)
        ) 

    @staticmethod
    def set_sta_param(param_str, value):
        if_name = CommandHelper.get_interface_name()

        return command_interpreter_obj.execute(
            Command.SET_STA_PARAM.value,
            [if_name, param_str, value],
        )

    @staticmethod
    def p2p_find():
        if_name = CommandHelper.get_interface_name()

        return CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} p2p_find").format(if_name)
        )

    @staticmethod
    def p2p_listen():
        if_name = CommandHelper.get_interface_name()

        return CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} p2p_listen").format(if_name)
        )

    @staticmethod
    def add_p2p_group(freq):
        if_name = CommandHelper.get_interface_name()

        return CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} p2p_group_add freq={}").format(if_name, freq)
        )

    @staticmethod
    def p2p_start_wps(pin_code):
        group_interface = CommandHelper.get_p2p_group_interface()
        if pin_code:
            return CommandHelper.run_shell_command(
                ("sudo wpa_cli -i {} wps_pin any {}").format(group_interface, pin_code)
            )
        else:    
            return CommandHelper.run_shell_command(
                ("sudo wpa_cli -i {} wps_pbc").format(group_interface)
            )

    @staticmethod
    def get_go_intent_value():
        return P2P_GO_INTENT

    @staticmethod
    def p2p_connect(addr, pin_code, method, conn_type, intent_value, he, persist):
        if_name = CommandHelper.get_interface_name()
        param_str = ""
        if pin_code:
            param_str += " {} {}".format(pin_code, method)
        else:
            param_str += " {}".format(method)
        if conn_type:
            if conn_type == P2PConnType.JOIN.value:
                param_str += " join"
            if conn_type == P2PConnType.AUTH.value: # Wait Peer GO NEG Req
                param_str += " auth go_intent={}".format(intent_value)
        else: # Send GO NEG Req
            param_str += " go_intent={}".format(intent_value)
        if he:
            param_str += " he"
        if persist:
            param_str += " persistent"

        return CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} p2p_connect {}{}").format(if_name, addr, param_str)
        )

    @staticmethod
    def p2p_invite(mac, persist, freq):
        p2p_dev_if = CommandHelper.get_p2p_dev_interface()
        if persist:
            # Assume persistent group id is 0
            param_str = "persistent=0"
            if freq:
                param_str += " freq={}".format(freq)

            return CommandHelper.run_shell_command(
                ("sudo wpa_cli -i {} p2p_invite {} peer={}").format(p2p_dev_if, param_str, mac)
            )
        else:
            group_if = CommandHelper.get_p2p_group_interface()
            return CommandHelper.run_shell_command(
                ("sudo wpa_cli -i {} p2p_invite group={} peer={}").format(p2p_dev_if, group_if, mac)
            )

    @staticmethod
    def stop_p2p_group(persist):
        if_name = CommandHelper.get_interface_name()
        group_interface = CommandHelper.get_p2p_group_interface()
        std_out, std_err = CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} p2p_group_remove {}").format(if_name, group_interface)
        )
        if persist:
            # Clear the persistent group with id 0
            p2p_dev_if = CommandHelper.get_p2p_dev_interface()
            std_out, std_err = CommandHelper.run_shell_command(
                ("sudo wpa_cli -i {} remove_network 0").format(p2p_dev_if)
            )
        return std_out, std_err

    @staticmethod
    def set_p2p_serv_disc(addr):
        p2p_dev_if = CommandHelper.get_p2p_dev_interface()
        if addr:
            # Send Service Discovery Req
            return CommandHelper.run_shell_command(
                ("sudo wpa_cli -i {} p2p_serv_disc_req {} 02000001").format(p2p_dev_if, addr)
            )
        else:
            # Enable/Add P2P Service
            # Add upnp in sample code
            return CommandHelper.run_shell_command(
                ("sudo wpa_cli -i {} p2p_service_add upnp 10 uuid:5566d33e-9774-09ab-4822-333456785632::urn:schemas-upnp-org:service:ContentDirectory:2").format(p2p_dev_if)
            )

    @staticmethod
    def set_p2p_ext_listen():
        # period: 1000, interval: 4000
        if_name = CommandHelper.get_interface_name()

        return CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} p2p_ext_listen 1000 4000").format(if_name)
        )

    @staticmethod
    def get_wsc_pin():
        if_name = CommandHelper.get_interface_name()

        return CommandHelper.run_shell_command(
            ("sudo wpa_cli -i {} wps_pin get").format(if_name)
        )
    
    @staticmethod
    def get_wsc_cred():
        # Get SSID, key_mgmt and Passphrase from config file
        key_list = ["ssid=", "psk=", "key_mgmt="]
        config_list = []
        with open(wpa_supplicant_config_file, "r") as config_f:
            config =config_f.read()
            for key in key_list:
                index = config.find(key)
                if index == -1:
                    DutLogger.log(LogCategory.ERROR,
                                "Cannot find the setting: {}".format(key))
                    return config_list, "Cannot find the setting"
                else:
                    index += len(key)
                    if config[index] == '\"':
                        #  the format aaaaa="xxxxxxxx"
                        index += 1
                        end = config[index:].find('\"')
                    else:
                        # the format bbbbb=yyyyyyyy
                        end = config[index:].find('\n')
                    config_list.append(config[index:index+end])
        return config_list, None


    
    @staticmethod
    def sta_start_wps(pin_code):
        if_name = CommandHelper.get_interface_name()
        if pin_code is not None:
            if len(pin_code) == 4 or len(pin_code) == 8:
                return CommandHelper.run_shell_command(
                    ("sudo wpa_cli -i {} wps_pin any {}").format(if_name, pin_code)
                )
            elif len(pin_code) == 1 and pin_code == '0':
                return CommandHelper.run_shell_command(
                    ("sudo wpa_cli -i {} wps_pin any").format(if_name)
                )
            else:
                DutLogger.log(LogCategory.ERROR, "Unrecognized PIN :" + pin_code)
                return "Failed", "Unrecognized PIN"
        else:    
            return CommandHelper.run_shell_command(
                ("sudo wpa_cli -i {} wps_pbc").format(if_name)
            )

    @staticmethod
    def sta_enable_wsc(config_enums: dict):
        """Method to enable WSC."""
        interface_name = CommandHelper.get_interface_name()
        StaCommandHelper.clear_supplicant_logs()

        CommandHelper.run_shell_command("sudo rfkill unblock wlan")
        CommandHelper.run_shell_command("sudo killall wpa_supplicant")
        CommandHelper.pause_execution(3)

        wpa_supplicant_config = "ctrl_interface=/var/run/wpa_supplicant\nap_scan=1\npmf=1\n"
 
        # Global settings
        for each_config_enum in config_enums:
            if each_config_enum in wpa_config_header:
                field_value = config_enums.get(each_config_enum)
                wpa_supplicant_config += each_config_enum + "=" + field_value + "\n"
        
        # WPS settings
        wps_enable = config_enums.get("wps_enable")
        if wps_enable is None:
                error = "No WPS_ENABLE TLV found. Failed to append STA WSC data"
                DutLogger.log(LogCategory.ERROR, error)
                return error
        else:
            wps_setting = CommandHelper.get_wps_settings(WpsDeviceRole.WPS_STA)
            if not wps_setting:
                error = "Failed to get STAUT WPS settings"
                DutLogger.log(LogCategory.ERROR, error)
                return error
            elif wps_enable == "1":
                # Enable Normal
                for cfg_item in wps_setting:
                    wpa_supplicant_config += cfg_item[0] + "=" + cfg_item[1] + "\n"
            else:
                error = "Invalid WPS TLV value: {}".format(wps_enable)
                DutLogger.log(LogCategory.ERROR, error)
                return error
            with open(wpa_supplicant_config_file, "w") as file:
                file.write(wpa_supplicant_config)

        supplicant_start_command = "sudo /usr/local/bin/WFA-Hostapd-Supplicant/wpa_supplicant -B -t -c {} -i {}".format(wpa_supplicant_config_file, interface_name)
        log_level = StaCommandHelper.__get_sta_debug_log_level()
        if log_level:
            supplicant_start_command += " {} -f {}".format(log_level, wpa_supplicant_log_folder_path)
        CommandHelper.run_shell_command(supplicant_start_command)

        return None