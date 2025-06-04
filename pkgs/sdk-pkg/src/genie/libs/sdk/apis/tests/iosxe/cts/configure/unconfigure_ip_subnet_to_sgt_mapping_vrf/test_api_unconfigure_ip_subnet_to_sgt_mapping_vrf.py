from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_ip_subnet_to_sgt_mapping_vrf
from unittest.mock import Mock


class TestUnconfigureIpSubnetToSgtMappingVrf(TestCase):

    def test_unconfigure_ip_subnet_to_sgt_mapping_vrf(self):
        self.device = Mock()
        result = unconfigure_ip_subnet_to_sgt_mapping_vrf(self.device, 'cisco','4.4.4.4','28','77')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no cts role-based sgt-map vrf cisco 4.4.4.4/28 sgt 77',)
        )

