from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_aggregate_address
from unittest.mock import Mock


class TestConfigureBgpAggregateAddress(TestCase):

    def test_configure_bgp_aggregate_address(self):
        self.device = Mock()
        result = configure_bgp_aggregate_address(self.device, 200, 'ipv6', '65::/48', True, 'v6aggregate', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 200', 'address-family ipv6', 'aggregate-address 65::/48 as-set suppress-map v6aggregate', 'exit-address-family'],)
        )
