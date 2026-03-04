from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_mld_vlan_immediate_leave

class TestUnconfigureIpv6MldVlanImmediateLeave(TestCase):

    def test_unconfigure_ipv6_mld_vlan_immediate_leave(self):
        device = Mock()
        result = unconfigure_ipv6_mld_vlan_immediate_leave(device, ' 1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ipv6 mld snooping vlan  1 immediate-leave'],)
        )