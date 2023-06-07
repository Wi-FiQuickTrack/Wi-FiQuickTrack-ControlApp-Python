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
""" Command Interpreter API """
import json
import os
import re
import subprocess
from .command import Command
from Commands.dut_logger import DutLogger, LogCategory


class CommandInterpreter:
    """
    Class used to load commands from commands.json file and run regex expression
    on the output of the command to extract the required information from the output.
    """

    def __init__(self):
        self.commands_json = None
        self.__load_commands_son()

    def __load_commands_son(self):
        """Reads & returns the commands json file."""
        dir_path = os.path.dirname(__file__)
        json_path = os.path.join(dir_path, "commands.json")
        with open(json_path) as commands_json:
            self.commands_json = json.load(commands_json)["commands"]

    def __json_obj_of_cmd_name(self, cmd_name):
        """
        json is intentionally not having the command names(cmd_name) as key as
        the equalent 'C' Language DUT doesn't have proper json dictionary to retrieve
        """
        for each_cmd_obj in self.commands_json:
            if cmd_name == each_cmd_obj["cmd_name"]:
                return each_cmd_obj
        return None

    def execute(self, cmd_name, cmd_args=[], regex_args=[]):
        """Takes the command input and executes it."""
        # getting command_timeout from settings set by user, in UI.
        # cmd_timeout = SettingsManager.get_setting_value(
        #     SettingsName.COMMAND_TIMEOUT)
        # cmd_args.insert(0, cmd_timeout)
        obj = self.__json_obj_of_cmd_name(cmd_name)

        if obj:
            res_arr = self.__execute_cmd_and_apply_regex(obj, cmd_args, regex_args)
            # if res_arr is not null and size is greater than 1 return res_arr[0]
            return str(res_arr[0]).strip() if len(res_arr) >= 1 else None
        else:
            DutLogger.log(LogCategory.ERROR, "Key {} does not exist".format(cmd_name))

    def __execute_cmd_and_apply_regex(self, obj, cmd_args, regex_args):
        """Executes the command and applies the regex to get the desired output."""
        shell_cmd = obj["cmd"]
        # format command with the dynamic arguments
        if len(cmd_args) != 0:
            str_cmd = shell_cmd.format(*cmd_args)
        else:
            str_cmd = shell_cmd
        # execute the command and get results
        status = subprocess.run(str_cmd, capture_output=True, shell=True, text=True)
        std_out = status.stdout
        std_err = status.stderr

        if not std_err:
            # DutLogger.log("\n---\n" + std_out + "\n\n")
            cmd_regex = obj["regex"]
            # regex_args = ""
            return self.__apply_regex(std_out, cmd_regex, regex_args)

        DutLogger.log(LogCategory.ERROR, "Error when running the command {}".format(shell_cmd) + std_err)
        return "--Error--"

    def __apply_regex(self, std_out, cmd_regex, regex_args):
        """Takes the command output and applies the regular expression."""
        if len(regex_args) == 0:
            str_regex = cmd_regex
        else:
            str_regex = cmd_regex.format(*regex_args)
            DutLogger.log(LogCategory.DEBUG, "Regex applied" + str_regex)
        res = re.findall(str_regex, std_out)
        # res = re.search(str_regex, std_out)
        return res
        # return res.group() if res is not None else None

    def execute_array(self, cmd_name, cmd_args=[], regex_args=[]):
        """Takes the command input and executes it."""
        obj = self.__json_obj_of_cmd_name(cmd_name)

        if obj:
            res_arr = self.__execute_cmd_and_apply_regex(obj, cmd_args, regex_args)
            # if res_arr is not null and size is greater than 1 return res_arr[0]
            return res_arr if len(res_arr) >= 1 else []
        else:
            DutLogger.log(LogCategory.DEBUG, "Key {} does not exist".format(cmd_name))

    def get_regex_used(self, cmd_name):
        """
        Parameters
        ----------
        cmd_name : str
                    [command_name to return the regex used]"""
        obj = self.__json_obj_of_cmd_name(cmd_name)
        return obj["regex"]

    def execute_and_return_all_occurrences(
        self, cmd_name: Command, cmd_args: list = [], regex_args: list = []
    ):
        """Takes in the command name to be executed along with parameters required for its execution
        and output parsing. Runs the command and returns all the occurrences of the regex match from the output.

        Parameters
        ----------
        cmd_name : str
            Name of the command to execute
        cmd_args : list, optional
            Arguments to be used for command execution
        regex_args : list, optional
            Arguments to be used for output parsing

        Returns
        -------
        array
            Parsed output of the command.
        """
        cmd_details = self.__get_json_for_cmd_name(cmd_name.value)
        if cmd_details:
            res_arr = self.__execute_cmd_and_apply_regex(
                cmd_details, cmd_args, regex_args
            )
            return res_arr if len(res_arr) >= 1 else []
        else:
            DutLogger.log(LogCategory.ERROR, "Key ({0}) doesn't exist".format(cmd_name.value))

    def apply_cmd_regex(
        self, cmd_name: Command, command_output: str, regex_args: list = []
    ):
        """Applies regex to the specified command output.

        ----------
        cmd_name : enum
                Name of the command for which output is to be parsed.
        cmd_output : [str]
                Output of the command.
        regex_args : [list]
                Arguments for the regex used to parse the command output.

        Returns
        -------
        str
            Parsed output of the command.
        """
        cmd_details = self.__get_json_for_cmd_name(cmd_name)
        regex = cmd_details["regex"]
        regex_parsed_output = self.__apply_regex(command_output, regex, regex_args)
        DutLogger.log(LogCategory.DEBUG, f"Regex parsed output is : {regex_parsed_output}")
        return regex_parsed_output[0] if len(regex_parsed_output) != 0 else None

    def __get_json_for_cmd_name(self, cmd_name: Command):
        """Gets the json object correspoding to a perticular command.Each json object\
           contains the name of the command, the actual CLI command and the regex to parse the required
           info from its CLI output.

        Parameters
        ----------
        cmd_name : Command
            Name of the command for which details are required.

        Returns
        -------
        json
            Details about the requested command.
        """
        for each_cmd_obj in self.commands_json:
            if cmd_name == each_cmd_obj["cmd_name"]:
                return each_cmd_obj
        return None
