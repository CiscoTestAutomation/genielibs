import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    remove_port_channel_interface,
)


class TestRemovePortChannelInterface(TestCase):

    def test_remove_port_channel_interface_with_integer(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = remove_port_channel_interface(device, 1)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no interface Port-channel1")

    def test_remove_port_channel_interface_with_string(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = remove_port_channel_interface(device, "10")

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no interface Port-channel10")


if __name__ == "__main__":
    unittest.main()
