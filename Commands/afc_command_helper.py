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

try:
    from .XXX_command_helper import XXX_CommandHelper as CommandHelper
except ImportError:
    from .command_helper import CommandHelper
from .shared_enums import CommandOperation, DebugLogLevel, QuickTrackRequestTLV, QuickTrackResponseTLV
from .command_interpreter import CommandInterpreter
from .command import Command
from Commands.dut_logger import DutLogger, LogCategory


class AfcCommandHelper:

    @staticmethod
    def afc_configure(config: dict):
        if QuickTrackRequestTLV.AFC_SERVER_URL in config:
            server_url = config.get(QuickTrackRequestTLV.AFC_SERVER_URL)
        else:
            return None, "Missed TLV: AFC_SERVER_URL"

        if QuickTrackRequestTLV.AFC_CA_CERT in config:
            ca_cert = config.get(QuickTrackRequestTLV.AFC_CA_CERT)
        else:
            return None, "Missed TLV: AFC_CA_CERT"

        if QuickTrackRequestTLV.SECURITY_TYPE in config:
            security_type = config.get(QuickTrackRequestTLV.SECURITY_TYPE)

        if QuickTrackRequestTLV.LOCATION_GEO_AREA in config:
            location_geo_area = config.get(QuickTrackRequestTLV.LOCATION_GEO_AREA)
            if location_geo_area == 0:
                center = config.get(QuickTrackRequestTLV.ELLIPSE_CENTER)
                major_axis = config.get(QuickTrackRequestTLV.ELLIPSE_MAJOR_AXIS)
                minor_axis = config.get(QuickTrackRequestTLV.ELLIPSE_MINOR_AXIS)
                orientation = config.get(QuickTrackRequestTLV.ELLIPSE_ORIENTATION)
            elif location_geo_area == 1:
                boundary = config.get(QuickTrackRequestTLV.LINEARPOLY_BOUNDARY)
            elif location_geo_area == 2:
                center = config.get(QuickTrackRequestTLV.RADIALPOLY_CENTER)
                boundary = config.get(QuickTrackRequestTLV.RADIALPOLY_BOUNDARY)

        return "Successful", None

    @staticmethod
    def afc_operation(config: dict):
        if QuickTrackRequestTLV.DEVICE_RESET in config:
            reset = config.get(QuickTrackRequestTLV.DEVICE_RESET)
            DutLogger.log(LogCategory.INFO, "Received AFC_OPERATION device_reset")

        if QuickTrackRequestTLV.SEND_SPECTRUM_REQ in config:
            req_type = config.get(QuickTrackRequestTLV.SEND_SPECTRUM_REQ)
            if req_type == 0:
                DutLogger.log(LogCategory.INFO, "Send Spectrum request with Channel and Frequency based")
            elif req_type == 1:
                DutLogger.log(LogCategory.INFO, "Send Spectrum request with Channel based")
            elif req_type == 2:
                DutLogger.log(LogCategory.INFO, "Send Spectrum request with Frequency based")
        
        if QuickTrackRequestTLV.POWER_CYCLE in config:
            power_cycle = config.get(QuickTrackRequestTLV.POWER_CYCLE)
            DutLogger.log(LogCategory.INFO, "Received AFC_OPERATION power_cycle")

        if QuickTrackRequestTLV.SEND_TEST_FRAME in config:
            type = config.get(QuickTrackRequestTLV.SEND_TEST_FRAME)
            if type == 0:
                DutLogger.log(LogCategory.INFO, "Trigger DUT to send test frames for 20MHz bandwidth")
            elif type == 1:
                DutLogger.log(LogCategory.INFO, "Trigger DUT to send test frames for 40MHz bandwidth")
            elif type == 2:
                DutLogger.log(LogCategory.INFO, "Trigger DUT to send test frames for 80MHz bandwidth")
            elif type == 3:
                DutLogger.log(LogCategory.INFO, "Trigger DUT to send test frames for 160MHz bandwidth")

        return "Successful", None

    @staticmethod
    def afc_get_info():
        # Get current center channel
        channel = 39
        freq = 5950 + 5 * channel
        
        info_dict = dict()
        info_dict[QuickTrackResponseTLV.OPER_CHANNEL] = channel
        info_dict[QuickTrackResponseTLV.OPER_FREQ] = freq

        return info_dict