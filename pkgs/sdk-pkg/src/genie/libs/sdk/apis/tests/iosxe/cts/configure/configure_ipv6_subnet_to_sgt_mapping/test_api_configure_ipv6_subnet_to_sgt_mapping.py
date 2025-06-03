from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_ipv6_subnet_to_sgt_mapping
from unittest.mock import Mock

class TestConfigureIpv6SubnetToSgtMapping(TestCase):

    def test_configure_ipv6_subnet_to_sgt_mapping(self):
        self.device = Mock()
        result = configure_ipv6_subnet_to_sgt_mapping(self.device, '2011:1::2', '64', '77')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('cts role-based sgt-map 2011:1::2/64 sgt 77',)
        )