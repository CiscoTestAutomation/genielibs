from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat64_nd_ra_prefix

class TestUnconfigureNat64NdRaPrefix(TestCase):

    def test_unconfigure_nat64_nd_ra_prefix(self):
        device = Mock()
        result = unconfigure_nat64_nd_ra_prefix(
            device,
            '2009::',
            '64',
            'TwentyFiveGigE1/0/23',
            '1',
            None, None, None, None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE1/0/23.1','no ipv6 nd ra nat64-prefix 2009::/64'],)
        )