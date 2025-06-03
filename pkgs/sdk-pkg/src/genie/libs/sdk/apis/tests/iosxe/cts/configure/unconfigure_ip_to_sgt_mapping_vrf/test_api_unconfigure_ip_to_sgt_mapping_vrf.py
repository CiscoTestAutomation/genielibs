from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_ip_to_sgt_mapping_vrf
from unittest.mock import Mock


class TestUnconfigureIpToSgtMappingVrf(TestCase):

    def test_unconfigure_ip_to_sgt_mapping_vrf(self):
        self.device = Mock()
        result = unconfigure_ip_to_sgt_mapping_vrf(self.device, 'cisco','4.4.4.4','77')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no cts role-based sgt-map vrf cisco 4.4.4.4 sgt 77',)
        )

