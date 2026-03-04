from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_mld_snooping_vlan_static_interface

class TestUnconfigureIpv6MldSnoopingVlanStaticInterface(TestCase):

    def test_unconfigure_ipv6_mld_snooping_vlan_static_interface(self):
        device = Mock()
        result = unconfigure_ipv6_mld_snooping_vlan_static_interface(device, '1', 'FF08::10', ' gi0/0')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (('no ipv6 mld snooping vlan 1 static FF08::10 interface  gi0/0',))
        )