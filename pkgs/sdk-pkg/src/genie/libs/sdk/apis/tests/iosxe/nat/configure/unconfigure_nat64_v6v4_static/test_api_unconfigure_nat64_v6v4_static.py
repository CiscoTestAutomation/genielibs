from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat64_v6v4_static

class TestUnconfigureNat64V6v4Static(TestCase):

    def test_unconfigure_nat64_v6v4_static(self):
        device = Mock()
        result = unconfigure_nat64_v6v4_static(device, '2009::2', '4.4.4.4', 'vrf1', None)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no nat64 v6v4 static 2009::2 4.4.4.4 vrf vrf1',)
        )