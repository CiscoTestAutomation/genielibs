import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vlan_shutdown


class TestConfigureVlanShutdown(unittest.TestCase):

    def test_configure_vlan_shutdown(self):
        device = Mock()

        result = configure_vlan_shutdown(device, 55)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vlan 55',
                'shutdown',
            ]
        )
