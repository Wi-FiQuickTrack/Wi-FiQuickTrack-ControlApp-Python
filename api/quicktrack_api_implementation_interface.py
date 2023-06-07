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
"""Abstraction class module."""
from abc import ABC, abstractmethod


class QuickTrackApiImplementationInterface(ABC):
    """
    Interface Abstraction Module.
    """

    def start_loop_back_server(self, tlvs_dict):
        pass

    def stop_loop_back_server(self):
        pass

    def get_ip_address(self):
        pass

    def get_mac_address(self, tlvs_dict):
        pass

    def get_dut_app_version_number(self):
        pass

    def sta_associate(self):
        pass

    def sta_disconnect(self):
        pass
    def create_new_interface_bridge_network(self, tlvs_dict):
        pass

    def assign_static_ip(self, tlvs_dict):
        pass

    def sta_configure(self, tlvs_dict):
        pass

    def sta_set_param(self, tlvs_dict):
        pass

    def sta_send_disconnect(self):
        pass

    def sta_reassociate(self):
        pass

    def sta_send_btm_query(self, tlvs_dict):
        pass

    def sta_send_anqp_query(self, tlvs_dict):
        pass

    def device_reset(self, tlvs_dict):
        pass
