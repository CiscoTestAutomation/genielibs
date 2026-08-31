import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_shutdown_vlan_interface_range,
)


class TestConfigureShutdownVlanInterfaceRange(unittest.TestCase):

    def test_configure_shutdown_vlan_interface_range(self):
        device = Mock()

        result = configure_shutdown_vlan_interface_range(device, 11, 20)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface range vlan 11-20',
                'shutdown',
            ]
        )
