import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vlan_name


class TestConfigureVlanName(unittest.TestCase):

    def test_configure_vlan_name(self):
        device = Mock()

        result = configure_vlan_name(device, '44', 'vlan44nameversion3')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vlan 44',
                'name vlan44nameversion3',
            ]
        )
