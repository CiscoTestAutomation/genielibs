from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_snooping_vlan_mrouter_interface

class TestUnconfigureIpIgmpSnoopingVlanMrouterInterface(TestCase):

    def test_unconfigure_ip_igmp_snooping_vlan_mrouter_interface(self):
        device = Mock()
        result = unconfigure_ip_igmp_snooping_vlan_mrouter_interface(device, 100, 'Gi1/0/10')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip igmp snooping vlan 100 mrouter interface Gi1/0/10',)
        )