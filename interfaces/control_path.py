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
from abc import ABC, abstractmethod


class ControlPath(ABC):
    """
    DUT control path interface.

    This class has to be implemented by any new control path implementation to
    work with the test tool.
    """

    @abstractmethod
    def start(self):
        """
        Start listening for API on the control path.
        """
        pass

    @abstractmethod
    def sendToClient(self):
        """
        Send back data to connected client
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stop listening for API on the control path.
        """
        pass
