from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_mac_access_group_mac_acl_in_out


class TestUnconfigureMacAccessGroupMacAclInOut(TestCase):

    def test_unconfigure_mac_access_group_mac_acl_in_out(self):
        self.device = Mock()
        unconfigure_mac_access_group_mac_acl_in_out(self.device, 'TenGigabitEthernet7/0/4', 'pacl1', 'in')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet7/0/4', 'no mac access-group pacl1 in'],)
        )
