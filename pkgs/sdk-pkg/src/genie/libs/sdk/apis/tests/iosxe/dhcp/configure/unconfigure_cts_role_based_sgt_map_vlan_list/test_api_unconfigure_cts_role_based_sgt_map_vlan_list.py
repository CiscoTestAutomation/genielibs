import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_cts_role_based_sgt_map_vlan_list


class TestUnconfigureCtsRoleBasedSgtMapVlanList(TestCase):

    def test_unconfigure_cts_role_based_sgt_map_vlan_list(self):
        device = Mock()
        result = unconfigure_cts_role_based_sgt_map_vlan_list(device, '300', '300')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with(['no cts role-based sgt-map vlan-list 300 sgt 300'])


if __name__ == '__main__':
    unittest.main()