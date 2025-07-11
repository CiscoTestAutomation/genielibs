from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_vlan_to_sgt_mapping
from unittest.mock import Mock


class TestUnconfigureVlanToSgtMapping(TestCase):

    def test_unconfigure_vlan_to_sgt_mapping(self):
        self.device = Mock()
        result = unconfigure_vlan_to_sgt_mapping(self.device, '100', '222')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts role-based sgt-map vlan-list 100 sgt 222'],)
        )
