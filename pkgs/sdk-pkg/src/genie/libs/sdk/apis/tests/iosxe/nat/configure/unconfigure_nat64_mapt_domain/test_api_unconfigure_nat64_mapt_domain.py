from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat64_mapt_domain
from unittest.mock import Mock


class TestUnconfigureNat64MaptDomain(TestCase):

    def test_unconfigure_nat64_mapt_domain(self):
        self.device = Mock()
        result = unconfigure_nat64_mapt_domain(self.device, '23')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no nat64 map-t domain 23',)
        )
