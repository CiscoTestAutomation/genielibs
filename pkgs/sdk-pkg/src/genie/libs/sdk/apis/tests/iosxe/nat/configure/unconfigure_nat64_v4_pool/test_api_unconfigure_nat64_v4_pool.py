from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat64_v4_pool

class TestUnconfigureNat64V4Pool(TestCase):

    def test_unconfigure_nat64_v4_pool(self):
        device = Mock()
        result = unconfigure_nat64_v4_pool(device, 'n64_pool', '172.0.0.1', '172.0.0.100')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no nat64 v4 pool n64_pool 172.0.0.1 172.0.0.100'],)
        )