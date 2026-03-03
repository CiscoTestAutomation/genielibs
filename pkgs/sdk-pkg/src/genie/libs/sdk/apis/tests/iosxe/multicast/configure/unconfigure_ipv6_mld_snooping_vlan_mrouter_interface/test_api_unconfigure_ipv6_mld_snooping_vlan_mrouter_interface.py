from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_mld_snooping_vlan_mrouter_interface

class TestUnconfigureIpv6MldSnoopingVlanMrouterInterface(TestCase):

    def test_unconfigure_ipv6_mld_snooping_vlan_mrouter_interface(self):
        device = Mock()
        result = unconfigure_ipv6_mld_snooping_vlan_mrouter_interface(device, '1', 'g0/0')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 mld snooping vlan 1 mrouter interface g0/0',)
        )