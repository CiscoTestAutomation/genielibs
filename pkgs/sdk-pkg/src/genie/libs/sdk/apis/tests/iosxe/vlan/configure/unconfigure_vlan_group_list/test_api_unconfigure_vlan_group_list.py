import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_vlan_group_list


class TestUnconfigureVlanGroupList(unittest.TestCase):

    def test_unconfigure_vlan_group_list(self):
        device = Mock()

        result = unconfigure_vlan_group_list(device, 'test', '10-40')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no vlan group test vlan-list 10-40'
        )
