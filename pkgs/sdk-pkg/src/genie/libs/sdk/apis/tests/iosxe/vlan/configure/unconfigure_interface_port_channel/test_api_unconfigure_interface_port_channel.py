import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    unconfigure_interface_port_channel,
)


class TestUnconfigureInterfacePortChannel(unittest.TestCase):

    def test_unconfigure_interface_port_channel(self):
        device = Mock()

        result = unconfigure_interface_port_channel(
            device,
            '5',
            '20',
            '30',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface port-channel 5',
                'no switchport private-vlan mapping 20 30',
            ]
        )
