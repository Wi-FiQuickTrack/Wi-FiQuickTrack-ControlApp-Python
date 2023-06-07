# Copyright (c) 2023 Wi-Fi Alliance

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

from .shared_enums import QuickTrackRequestTLV, QuickTrackResponseTLV
from .command import ApiInterface, ApiReturnStatus, Command
try:
    from .XXX_afc_command_helper import XXX_AfcCommandHelper as AfcCommandHelper
except ImportError:
    from .afc_command_helper import AfcCommandHelper
from Commands.dut_logger import DutLogger, LogCategory

class AFCD_CONFIGURE(ApiInterface):
    def execute(self):
        """Method to execute the AFC configure command."""
        self.std_out, self.std_err = AfcCommandHelper.afc_configure(self.params)

    def get_return_status(self):
        """Method to return the return status of AFC configure based on the std_err."""
        if self.std_err is None:
            return ApiReturnStatus(0, "AFC configure completed : " + str(self.std_out))
        else:
            return ApiReturnStatus(
                1, "Unable to configure AFC commands.[" + str(self.std_err) + "]"
            )

class AFCD_OPERATION(ApiInterface):
    def execute(self):
        """Method to execute the AFC operation command."""
        self.std_out, self.std_err = AfcCommandHelper.afc_operation(self.params)

    def get_return_status(self):
        """Method to return the return status of AFC operation based on the std_err."""
        if self.std_err is None:
            return ApiReturnStatus(0, "AFC operation completed : " + str(self.std_out))
        else:
            return ApiReturnStatus(
                1, "Unable to execute AFC operation commands. [" + str(self.std_err) + "]"
            )

class AFCD_GET_INFO(ApiInterface):
    def execute(self):
        """Method to execute and get the AFC required information ."""

        self.std_out = AfcCommandHelper.afc_get_info()
        if QuickTrackResponseTLV.OPER_CHANNEL not in self.std_out:
            self.std_err = "failed to get operation channel info"
            return

        if QuickTrackResponseTLV.OPER_FREQ not in self.std_out:
            self.std_err = "failed to get operation frequency info"

    def get_return_status(self):
        """Returns the return status with the status code with following description.

        status code:
        0 - success, returns successful.
        1- Failure, unable to get the AFC information, returns None."""
        if self.std_err is None:
            return ApiReturnStatus(
                0,
                "Successful to get AFC required information",
                self.std_out
            )
        else:
            return ApiReturnStatus(1, str(self.std_err))
