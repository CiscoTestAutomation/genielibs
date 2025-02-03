from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_mapt_domain
from unittest.mock import Mock


class TestConfigureNat64MaptDomain(TestCase):

    def test_configure_nat64_mapt_domain(self):
        self.device = Mock()
        result = configure_nat64_mapt_domain(self.device, '23', '2A02:C79:FC03:43::/64', '2A02:C7A:E460::/43', '100.67.8.0/22', '8', None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['nat64 map-t domain 23', 'default-mapping-rule 2A02:C79:FC03:43::/64', 'basic-mapping-rule', 'ipv6-prefix 2A02:C7A:E460::/43', 'ipv4-prefix 100.67.8.0/22', 'port-parameters share-ratio 8'],)
        )
