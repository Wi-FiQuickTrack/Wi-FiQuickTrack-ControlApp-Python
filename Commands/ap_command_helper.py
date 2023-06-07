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
from .shared_enums import CommandOperation, DebugLogLevel, BssIdentifierBand, WpsDeviceRole
from .command_interpreter import CommandInterpreter
from .command import Command
from datetime import datetime
from Commands.dut_logger import DutLogger, LogCategory
import os
from datetime import datetime

command_interpreter_obj = CommandInterpreter()
store_hostapd_config_for_debug = False
ap_debug_log_level = DebugLogLevel.DISABLE
hostapd_log_folder_path = "/var/log/hostapd.log"
hostapd_config_path = "/etc/hostapd/hostapd.conf"
hostapd_config_files = []


class ApCommandHelper:
    store_test_artifcats = False

    @staticmethod
    def create_hostapd_config(configuration: dict, append_config_file: bool):
        """Creates and writes the hostapd configurations received to configuration file in /etc/hostapd/.

        Parameters
        ----------
        configuration : dict
            Configurations to be configured

        merge_config_file : bool
            Flag to indicate if new hostapd config file has to be create or the new config has to be merged into existing file

        """
        global hostapd_config_files
        if not append_config_file:
            hostapd_file_name = "hostapd.conf"
            if "hostapd_file_name" in configuration:
                hostapd_file_name = configuration.pop("hostapd_file_name")
            hostapd_config_files.append(hostapd_file_name)
        else:
            hostapd_file_name = hostapd_config_files[0]

        if "interface_name" in configuration:
            interface_name = configuration.pop("interface_name")
        else:
            interface_name = CommandHelper.get_interface_name()

        hostapd_config, std_err = ApCommandHelper.get_hostapd_config(
            configuration, interface_name, append_config_file
        )
        if std_err is None:
            try:
                now = datetime.now()
                dt_string = now.strftime("%d%m%Y_%H:%M:%S")

                if not append_config_file:
                    DutLogger.log(LogCategory.DEBUG, "Writing the following configuration into Hostapd file:\n" + str(hostapd_config))
                    with open(("/etc/hostapd/{}").format(hostapd_file_name), "w+") as file:
                        file.write(hostapd_config)
                else:
                    DutLogger.log(LogCategory.DEBUG, "Appending the following configuration into Hostapd file:\n" + str(hostapd_config))
                    with open(("/etc/hostapd/{}").format(hostapd_file_name), "a") as file:
                        file.write(hostapd_config)

                if store_hostapd_config_for_debug:
                    hostapd_file_path = "/etc/hostapd/hostapd_files"
                    if not os.path.exists(hostapd_file_path):
                        os.mkdir(hostapd_file_path)
                    try:
                        with open(
                            "/etc/hostapd/hostapd_files/hostapd" + str(dt_string), "w+"
                        ) as file:
                            file.write(hostapd_config)
                    except IOError as err:
                        DutLogger.log(LogCategory.ERROR, "Error when creating hostapd debug file:" + str(err))
            except IOError as err:
                DutLogger.log(LogCategory.ERROR, "Error writing into Hostapd file:\n" + str(err))
                return None, str(err)
            return "Configuration file created", None
        else:
            DutLogger.log(LogCategory.ERROR, "Error creating Hostapd file:\n" + str(std_err))
            return None, "Unable to create hostapd configuration."

    @staticmethod
    def store_hostapd_config():
        """Stores the existing hostapd configuration in /var/log folder"""
        global hostapd_config_files
        if hostapd_config_files:
            qt_configs_folder = "/var/log/qt_configs/"
            if not os.path.exists(qt_configs_folder):
                CommandHelper.run_shell_command("sudo mkdir {}".format(qt_configs_folder))
            for each_hostapd_config in hostapd_config_files:
                now = datetime.now()
                dt_string = now.isoformat()
                CommandHelper.run_shell_command("sudo mv /etc/hostapd/{} {}hostapd_{}.conf".format(each_hostapd_config, qt_configs_folder, dt_string))

    @staticmethod
    def get_existing_hostapd_conf():
        """Returns the existing hostapd configuration that was previously configured."""
        existing_config = {}
        if os.path.exists(hostapd_config_path):
            with open(hostapd_config_path) as file_reader:
                for each_line in file_reader:
                    key, val = each_line.split("=")
                    existing_config[key] = val.rstrip()
        return existing_config

    @staticmethod
    def get_hostapd_config(tlv_values: dict, interface_name: str, append_config_file: bool):
        """Returns the hostapd configurations from TLV's(type-length-value) to string that will be written into configuration file .

        Parameters
        ----------
        tlv_values : dict
            Configurations in TLVs
        interface_name:str
            Interface name to be configured.
        merge_config_file : bool
            Flag to indicate if new hostapd config file has to be create or the new config has to be merged into existing file
        """
        if interface_name is None:
            return None, "Unable to get interface name."
        if append_config_file:
            hostapd_config = (
                "bss=" + interface_name +"\nctrl_interface=/var/run/hostapd"
            )
        else:
            hostapd_config = (
                "ctrl_interface=/var/run/hostapd\nctrl_interface_group=0\ninterface=" + interface_name
            )
        has_sae = False
        has_wpa = False
        has_pmf = False
        has_owe = False
        has_transition = False
        band = None
        channel = None
        chwidth = 1
        enable_ax = enable_ac = False
        chwidthset = vht_chwidthset = False
        enable_muedca = False
        has_sae_groups = False
        enable_wps = False
        use_mbss = False
        for tlv_value in tlv_values:
            if tlv_value == "wpa_key_mgmt" and "SAE" in tlv_values[tlv_value] and "WPA-PSK" in tlv_values[tlv_value]:
                has_transition = True
            if tlv_value == "wpa_key_mgmt" and "OWE" in tlv_values[tlv_value]:
                has_owe = True
            if tlv_value == "wpa_key_mgmt" and "SAE" in tlv_values[tlv_value]:
                has_sae = True
            if tlv_value == "wpa" and "2" in tlv_values[tlv_value]:
                has_wpa = True
            if tlv_value == "ieee80211w":
                has_pmf = True
            if tlv_value == "hw_mode":
                band = tlv_values[tlv_value]
            if tlv_value == "channel":
                channel = int(tlv_values[tlv_value])
            if tlv_value == "he_oper_chwidth":
                chwidth = int(tlv_values[tlv_value])
                chwidthset = True
            if tlv_value == "vht_oper_chwidth":
                chwidth = int(tlv_values[tlv_value])
                vht_chwidthset = True
            if tlv_value == "ieee80211ac" and "1" in tlv_values[tlv_value]:
                enable_ac = True
            if tlv_value == "ieee80211ax" and "1" in tlv_values[tlv_value]:
                enable_ax = True
            if tlv_value == "he_mu_edca":
                enable_muedca = True
            if tlv_value == "sae_groups":
                has_sae_groups = True
            if tlv_value == "bss_identifier":
                use_mbss = True
                continue
            if tlv_value == "wps_enable":
                wps_setting = CommandHelper.get_wps_settings(WpsDeviceRole.WPS_AP)
                enable_wps = True
                if tlv_values[tlv_value] == "1":
                    # Normal, set wps state and wps common settings
                    for cfg_item in wps_setting:
                        if cfg_item[2][0] == "1":
                            # OOB only
                            if cfg_item[0] == "wps_state":
                                hostapd_config += "\n" + cfg_item[0] + "=" + "2"
                        elif cfg_item[2][0] == "2":
                            # Common settings
                            hostapd_config += "\n" + cfg_item[0] + "=" + cfg_item[1]
                elif tlv_values[tlv_value] == "2":
                    # OOB, set all settings
                    DutLogger.log(LogCategory.INFO, "APUT Configure WPS: OOB.")
                    for cfg_item in wps_setting:
                        hostapd_config += "\n" + cfg_item[0] + "=" + cfg_item[1]
                else:
                    DutLogger.log(LogCategory.ERROR, "Unknown WPS TLV value: {}".format(tlv_values[tlv_value]))
                continue

            if tlv_value == "owe_transition_bss_identifier":
                bss_id = int(tlv_values[tlv_value])
                bss_band = bss_id & 0x0F
                identifier = (bss_id & 0xF0) >> 4
                owe_if = CommandHelper.get_interface_name(identifier)
                if not owe_if:
                    owe_if = CommandHelper.set_interface_bss_id(band=bss_band, bss_id=identifier)
                if owe_if:
                    hostapd_config += "\n" + "owe_transition_ifname" + "=" + owe_if
                    if has_owe:
                        hostapd_config += "\n" + "ignore_broadcast_ssid=1"
                else:
                    DutLogger.log(LogCategory.ERROR, "Can't find owe transition ifname")
            elif tlv_value == "transition_disable":
                hostapd_config += "\n" + tlv_value + "=" + hex(int(tlv_values[tlv_value]))
            elif tlv_value == "auth_algorithm":
                hostapd_config += "\n" + "auth_algs" + "=" + tlv_values[tlv_value]
            elif tlv_value == "he_mu_edca":
                hostapd_config += "\n" + "he_mu_edca_qos_info_param_count" + "=" + tlv_values[tlv_value]
            else:
                hostapd_config += "\n" + tlv_value + "=" + tlv_values[tlv_value]

        if not has_pmf:
            if has_transition:
                hostapd_config += "\nieee80211w=1"
            elif has_sae and has_wpa:
                hostapd_config += "\nieee80211w=2"
            elif has_owe:
                hostapd_config += "\nieee80211w=2"
            elif has_wpa:
                hostapd_config += "\nieee80211w=1"
        if has_sae:
            hostapd_config += "\nsae_require_mfp=1"
        # Note: if any new DUT configuration is added for sae_groups,
        # then the following unconditional sae_groups addition should be
        # changed to become conditional on there being no other sae_groups
        # configuration
        # e.g.:
            if not has_sae_groups:
                hostapd_config += "\nsae_groups=15 16 17 18 19 20 21"

        # Todo: Add 6G conf
        #Channel width configuration
        #Default: 20MHz in 2.4G(No configuration required) 80MHz in 5G
        if band == "a":
            if __class__.is_ht40plus_chan(channel):
                hostapd_config += "\nht_capab=[HT40+]"
            elif __class__.is_ht40minus_chan(channel):
                hostapd_config += "\nht_capab=[HT40-]"
            else:
                chwidth = 0    
            if chwidth > 0:
                center_freq = ApCommandHelper.get_center_freq_idx(channel, chwidth)
                if enable_ac:
                    if vht_chwidthset == False:
                        hostapd_config += "\nvht_oper_chwidth="+str(chwidth)
                    hostapd_config += "\nvht_oper_centr_freq_seg0_idx="+str(center_freq)
                if enable_ax:
                    if chwidthset == False:
                        hostapd_config += "\nhe_oper_chwidth="+str(chwidth)
                    hostapd_config += "\nhe_oper_centr_freq_seg0_idx="+str(center_freq)

        if enable_muedca:
            hostapd_config += "\nhe_mu_edca_qos_info_queue_request=1"
            hostapd_config += "\nhe_mu_edca_ac_be_aifsn=0"
            hostapd_config += "\nhe_mu_edca_ac_be_ecwmin=15"
            hostapd_config += "\nhe_mu_edca_ac_be_ecwmax=15"
            hostapd_config += "\nhe_mu_edca_ac_be_timer=255"
            hostapd_config += "\nhe_mu_edca_ac_bk_aifsn=0"
            hostapd_config += "\nhe_mu_edca_ac_bk_aci=1"
            hostapd_config += "\nhe_mu_edca_ac_bk_ecwmin=15"
            hostapd_config += "\nhe_mu_edca_ac_bk_ecwmax=15"
            hostapd_config += "\nhe_mu_edca_ac_bk_timer=255"
            hostapd_config += "\nhe_mu_edca_ac_vi_ecwmin=15"
            hostapd_config += "\nhe_mu_edca_ac_vi_ecwmax=15"
            hostapd_config += "\nhe_mu_edca_ac_vi_aifsn=0"
            hostapd_config += "\nhe_mu_edca_ac_vi_aci=2"
            hostapd_config += "\nhe_mu_edca_ac_vi_timer=255"
            hostapd_config += "\nhe_mu_edca_ac_vo_aifsn=0"
            hostapd_config += "\nhe_mu_edca_ac_vo_aci=3"
            hostapd_config += "\nhe_mu_edca_ac_vo_ecwmin=15"
            hostapd_config += "\nhe_mu_edca_ac_vo_ecwmax=15"
            hostapd_config += "\nhe_mu_edca_ac_vo_timer=255"
        
        if enable_wps:
            if use_mbss:
               hostapd_config += "\nwps_rf_bands=ag"
            else: 
                if band == "a":
                    hostapd_config += "\nwps_rf_bands=a"
                elif band == "g":
                    hostapd_config += "\nwps_rf_bands=g"

        '''
        if merge_config_file:
            appended_hostapd_conf_str = ""
            existing_conf = ApCommandHelper.get_existing_hostapd_conf()
            hostapd_config_dict = ApCommandHelper.__convert_config_str_to_dict(config=hostapd_config)
            for each_key in existing_conf:
                if each_key not in hostapd_config_dict:
                    hostapd_config_dict[each_key] = existing_conf[each_key]
            for each_hostapd_conf in hostapd_config_dict:
                appended_hostapd_conf_str += each_hostapd_conf + "=" + hostapd_config_dict[each_hostapd_conf] + "\n"
            hostapd_config = appended_hostapd_conf_str.rstrip()
        '''

        hostapd_config += "\n"
        return hostapd_config, None

    @staticmethod
    def __convert_config_str_to_dict(config: str):
        """Converting string into dictionary using dict comprehension
        Parameters
        -----------
        config : [str]
            Converts the configuration from datatype string to dictionary.
        """
        config_dict = dict(each_config.split("=") for each_config in config.split("\n"))
        return config_dict


    @staticmethod
    def ap_start_up():
        """Starts the hostapd service on the AP."""
        global hostapd_config_files
        #ApCommandHelper.store_test_artifcats = True
        debug_log_level = ApCommandHelper.__get_ap_debug_log_level()
        now = datetime.now()
        dt_string = now.isoformat()

        ApCommandHelper.__killall_hostapd()
        ApCommandHelper.clear_hostapd_logs()
        std_out, std_err = CommandHelper.run_shell_command("hostapd -v")
        if std_err is None:
            #Create new interfaces

            hostapd_start_command = "/usr/local/bin/WFA-Hostapd-Supplicant/hostapd -B -t -g /run/hostapd-global"
            for each_hostapd_file in hostapd_config_files:
                hostapd_start_command += " /etc/hostapd/{}".format(each_hostapd_file)

            if debug_log_level:
                hostapd_start_command += " -f {} {}".format(hostapd_log_folder_path, debug_log_level)
            CommandHelper.run_shell_command(hostapd_start_command)
            CommandHelper.pause_execution(3)

            if CommandHelper.BSSID_COUNT > 1: # More then one wlan interface
                std_out, std_err = CommandHelper.create_new_interface_bridge_network()
                if std_err is not None:
                    return None, "Error when creating new interface: {}".format(std_err)
                CommandHelper.add_all_interfaces_to_bridge()
            status = ApCommandHelper.check_hostapd_is_active()
            if status:
                return "Hostapd service is active", None
            else:
                return None, "Unable to start hostapd service."
        else:
            return None, "Hostapd service is not installed." + str(std_out)

    @staticmethod
    def ap_stop():
        CommandHelper.clear_bss_identifiers()
        """Stops the hostapd service on the AP."""
        global hostapd_config_files
        if ApCommandHelper.store_test_artifcats:
            ApCommandHelper.store_hostapd_config()
            #ApCommandHelper.__log_hostapd_logs()
            ApCommandHelper.store_test_artifcats = False
        hostapd_config_files = []
        status = ApCommandHelper.check_hostapd_is_active()
        if status:
            CommandHelper.run_shell_command("sudo rfkill unblock wlan")
            interface_name = CommandHelper.get_interface_name()
            ApCommandHelper.__killall_hostapd()
            CommandHelper.pause_execution(3)
            status = ApCommandHelper.check_hostapd_is_active()

            if not status:
                return "Hostapd service is inactive.", None
            else:
                return None, "Unable to stop hostapd service."
        else:
            return "Hostapd service is inactive.", None

    @staticmethod
    def __log_hostapd_logs():
        """Logs the hostapd debug logs into a text file for debug."""
        global ap_debug_log_level
        if ap_debug_log_level != DebugLogLevel.DISABLE :
            if os.path.exists(hostapd_log_folder_path):
                with open(hostapd_log_folder_path, "r") as file_reader:
                    file_content = file_reader.readlines()
                    if file_content:
                        DutLogger.log(LogCategory.DEBUG, "Hostapd logs :" + str(file_content))
            else:
                DutLogger.log(LogCategory.DEBUG, "Hostapd debug log file is not found at {}".format(hostapd_log_folder_path))

    @staticmethod
    def __get_ap_debug_log_level():
        global ap_debug_log_level
        if ap_debug_log_level == DebugLogLevel.BASIC:
            return "-dK"
        elif ap_debug_log_level == DebugLogLevel.ADVANCED:
            return "-dddK"
        else:
            return None

    @staticmethod
    def set_ap_debug_log_level(log_level):
        global ap_debug_log_level
        ap_debug_log_level = log_level

    @staticmethod
    def check_hostapd_is_active():
        """Utility method to check if hostapd service is active

        Returns
        -------
        bool
            Boolean representing if hostapd service is active or not.
        """
        res, _ = CommandHelper.run_shell_command("sudo pidof hostapd")
        if res:
            return True
        else:
            DutLogger.log(LogCategory.DEBUG, "Hostapd service is inactive.")
            return False

    @staticmethod
    def __killall_hostapd():
        CommandHelper.run_shell_command("sudo killall hostapd")

    @staticmethod
    def clear_hostapd_logs():
        """Method to remove the hostapd logs before script execution."""
        if os.path.exists(hostapd_log_folder_path):
            CommandHelper.run_shell_command(
                ("sudo rm -rf {}").format(hostapd_log_folder_path)
            )

    @staticmethod
    def get_ap_if_status(if_name):
        hostapd_cli_status, _ = CommandHelper.run_shell_command(
            "sudo hostapd_cli -i {} status".format(if_name)
        )
        interface_freq = command_interpreter_obj.apply_cmd_regex(
            Command.GET_FREQ, hostapd_cli_status
        )
        interface_ssid = command_interpreter_obj.apply_cmd_regex(
            Command.GET_AP_SSID, hostapd_cli_status
        )
        mac_addr = command_interpreter_obj.apply_cmd_regex(
            Command.GET_AP_DUT_MAC_ADDR, hostapd_cli_status
        )
        return interface_freq, interface_ssid, mac_addr

    @staticmethod
    def get_center_freq_idx(chan, width: int = 1):
        if (width == 1):
            if chan >= 36 and chan <= 48:
                return "42"
            elif chan <= 64:
                return "58"
            elif chan >= 100 and chan <= 112:
                return "106"
            elif chan <= 128:
                return "122"
            elif chan <= 144:
                return "138"
            elif chan >= 149 and chan <= 161:
                return  "155"
        elif (width == 2):
            if chan >= 36 and chan <= 64:
                return "50"
            elif chan >= 100 and chan <= 128:
                return "114"

    @staticmethod
    def is_ht40plus_chan(chan):
        if (chan == 36 or chan == 44 or chan == 52 or chan == 60 or
            chan == 100 or chan == 108 or chan == 116 or chan == 124 or
            chan == 132 or chan == 140 or chan == 149 or chan == 157):
            return True
        else:
            return False

    @staticmethod
    def is_ht40minus_chan(chan):
        if (chan == 40 or chan == 48 or chan == 56 or chan == 64 or
            chan == 104 or chan == 112 or chan == 120 or chan == 128 or
            chan == 136 or chan == 144 or chan == 153 or chan == 161):
            return True
        else:
            return False

    '''
    @staticmethod
    def store_bss_identifiers(bss_identifier: int, ssid: str, interface_name):
        global bss_identifiers
        bss_identifiers[bss_identifier] = (ssid, interface_name)

    @staticmethod
    def get_bss_identifier_details(identifier: int):
        global bss_identifiers
        if identifier in bss_identifiers:
            return bss_identifiers[identifier]
        return None, None

    @staticmethod
    def get_bss_identifiers():
        global bss_identifiers
        return bss_identifiers
    '''

    @staticmethod
    def send_ap_disconnect(address):
        if_name = CommandHelper.get_interface_name()
        reason = "reason=1"
        return CommandHelper.run_shell_command(
            ("sudo hostapd_cli -i {} disassociate {} {}").format(if_name, address, reason)
        )
    
    @staticmethod
    def ap_chan_switch(channel, freq):
        if_name = CommandHelper.get_interface_name()
        center_freq = 5000 + int(__class__.get_center_freq_idx(int(channel))) * 5
        if center_freq == int(freq) + 30 or center_freq == int(freq) - 10:
            offset = 1
        else:
            offset = -1
        return CommandHelper.run_shell_command(
            ("sudo hostapd_cli -i {} chan_switch 10 {} center_freq1={} sec_channel_offset={} bandwidth=80 vht").format(if_name, freq, center_freq, offset)
        )

    @staticmethod
    def send_ap_btm_req(bssid, disassoc_immi, cand_list, disassoc_timer, retry_delay, bss_term_bit, bss_term_tsf, bss_term_duration):
        param_str = ""
        if disassoc_immi:
            param_str += " disassoc_imminent={}".format(disassoc_immi)
        if cand_list:
            if int(cand_list) == 1:
                param_str += " pref=1"
        if disassoc_timer:
            param_str += " disassoc_timer={}".format(disassoc_timer)
        if retry_delay:
            param_str += " mbo=0:{}:0".format(retry_delay)

        # ToDo: BSS termination is not yet finished
        if bss_term_bit and bss_term_tsf and bss_term_duration:
            param_str += " bss_term={},{}".format(bss_term_tsf, bss_term_duration)        
        DutLogger.log(LogCategory.DEBUG, "ap_btm_req param: {}".format(param_str))
        interface_name = CommandHelper.get_interface_name()

        return command_interpreter_obj.execute(
            Command.SEND_AP_BTM_REQ.value,
            [interface_name, bssid, param_str],
        )

    @staticmethod
    def set_ap_param(param_str, value):
        if_name = CommandHelper.get_interface_name()

        return  command_interpreter_obj.execute(
            Command.SET_AP_PARAM.value,
            [if_name, param_str, value],
        )

    @staticmethod
    def get_wsc_cred():
        # Get SSID, key_mgmt and Passphrase from config file
        key_list = ["ssid=", "wpa_passphrase=", "wpa_key_mgmt="]
        config_list = []
        file_path = "/etc/hostapd/{}".format(hostapd_config_files[0])
        with open(file_path, "r") as config_f:
            config =config_f.read()
            for key in key_list:
                index = config.find(key)
                if index == -1:
                    DutLogger.log(LogCategory.INFO, "Cannot find the setting: {}".format(key))
                    config_list.append("")
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
    def ap_start_wps(pin_code):
        if_name = CommandHelper.get_interface_name()
        if pin_code is not None:
            # Verify invalid PIN code
            if os.path.exists("/tmp/pin_checksum.sh"):
                std_out, std_err = CommandHelper.run_shell_command("/tmp/pin_checksum.sh {}".format(pin_code))
            else:
                std_out = "1"
            if std_out and int(std_out):
                return CommandHelper.run_shell_command(
                    ("sudo hostapd_cli -i {} wps_pin any {}").format(if_name, pin_code)
                )
            else:
                error = "AP detects invalid PIN code"
                DutLogger.log(LogCategory.ERROR, "Invalid PIN code :" + pin_code)
                return "Failed", error
        else:    
            return CommandHelper.run_shell_command(
                ("sudo hostapd_cli -i {} wps_pbc").format(if_name)
            )

    @staticmethod
    def ap_configure_wsc(config_enums: dict):
        __class__.ap_stop()
        config_only = config_enums.pop("wsc_config_only", None)
        ApCommandHelper.assign_interface_and_config_file_name(config_enums)
        __class__.create_hostapd_config(config_enums, False)
        if config_only is not None:
            return "Configure wsc ap successfully. (Configure only)", None
        
        __class__.ap_start_up()
        return "Confiugre and start wsc ap successfully. (Configure and start)", None

    @staticmethod
    def get_wsc_pin():
        if_name = CommandHelper.get_interface_name()

        return CommandHelper.run_shell_command(
            ("sudo hostapd_cli -i {} wps_ap_pin get").format(if_name)
        )

    @staticmethod
    def assign_interface_and_config_file_name(config: dict):
        append_file = False
        if "bss_identifier" in config:
            bss_identifier = int(config.get("bss_identifier"))

            band = bss_identifier & 0x0F
            identifier = (bss_identifier & 0xF0) >> 4
            multiple_bssid = (bss_identifier & 0x100) >> 8
            transmitter = (bss_identifier & 0x200) >> 9
            hostapd_file_name = ""

            if band == BssIdentifierBand._24GHz.value:
                hostapd_file_name = "hostapd_24G_"
            elif band == BssIdentifierBand._5GHz.value:
                hostapd_file_name = "hostapd_5G_"
            elif band == BssIdentifierBand._6GHz.value:
                hostapd_file_name = "hostapd_6G_"
            hostapd_file_name += str(identifier) + ".conf"
            config["hostapd_file_name"] = hostapd_file_name
            # Get if_name from bss_id. If not exist assign id
            interface_name = CommandHelper.get_interface_name(identifier)
            if not interface_name:
                interface_name = CommandHelper.set_interface_bss_id(band=band, bss_id=identifier)
            if multiple_bssid:
                DutLogger.log(LogCategory.ERROR, "MBSSID is not fully supported. Platform dependent")
                return False
                # Need platform support MBSSID to append file
                if not transmitter:
                    append_file = True
        else:
            if "he_6g_only" in config:
                band = BssIdentifierBand._6GHz.value
            else:
                hw_mode = config["hw_mode"]
                if hw_mode == "a":
                    band = BssIdentifierBand._5GHz.value
                else:
                    band = BssIdentifierBand._24GHz.value
            # Single Wlan use ID 1
            # WPS will configure twice so try to get if with ID 1 first
            interface_name = CommandHelper.get_interface_name(bss_id=1)
            if not interface_name:
                interface_name = CommandHelper.set_interface_bss_id(band=band, bss_id=1)
        config["interface_name"] = interface_name
        return append_file

    @staticmethod
    def ap_configure(config: dict):
        # Parse BSS_IDENTIFIER TLV in multiple WLANs case
        append_file = ApCommandHelper.assign_interface_and_config_file_name(config)
        return ApCommandHelper.create_hostapd_config(config, append_file)