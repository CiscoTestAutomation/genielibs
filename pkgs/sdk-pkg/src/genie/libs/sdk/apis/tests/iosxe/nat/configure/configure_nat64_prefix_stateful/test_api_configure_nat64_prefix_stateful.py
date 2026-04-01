from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_prefix_stateful

class TestConfigureNat64PrefixStateful(TestCase):

    def test_configure_nat64_prefix_stateful(self):
        device = Mock()
        result = configure_nat64_prefix_stateful(
            device,
            '2002:0001:0000:0000:0000:0000:0000:0000',
            '96',
            None,
            'vrf1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('nat64 prefix stateful 2002:0001:0000:0000:0000:0000:0000:0000/96 vrf vrf1',)
        )