from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat64_prefix_stateful

class TestUnconfigureNat64PrefixStateful(TestCase):

    def test_unconfigure_nat64_prefix_stateful(self):
        device = Mock()
        result = unconfigure_nat64_prefix_stateful(
            device,
            None,
            '2002:0001:0000:0000:0000:0000:0000:0000',
            '96',
            'vrf1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no nat64 prefix stateful 2002:0001:0000:0000:0000:0000:0000:0000/96 vrf vrf1',)
        )