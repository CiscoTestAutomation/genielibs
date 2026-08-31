import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vlan_group_list


class TestConfigureVlanGroupList(unittest.TestCase):

    def test_configure_vlan_group_list(self):
        device = Mock()

        result = configure_vlan_group_list(device, 'test', '10-40')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'vlan group test vlan-list 10-40'
        )
