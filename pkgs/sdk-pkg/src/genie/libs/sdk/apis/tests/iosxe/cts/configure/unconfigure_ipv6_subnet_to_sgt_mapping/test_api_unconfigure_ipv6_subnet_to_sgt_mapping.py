from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_ipv6_subnet_to_sgt_mapping
from unittest.mock import Mock


class TestUnconfigureIpv6SubnetToSgtMapping(TestCase):

    def test_unconfigure_ipv6_subnet_to_sgt_mapping(self):
        self.device = Mock()
        result = unconfigure_ipv6_subnet_to_sgt_mapping(self.device, '2011:1::2','64','77')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no cts role-based sgt-map 2011:1::2/64 sgt 77',)
        )

