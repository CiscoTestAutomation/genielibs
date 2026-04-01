from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_v4_pool

class TestConfigureNat64V4Pool(TestCase):

    def test_configure_nat64_v4_pool(self):
        device = Mock()
        result = configure_nat64_v4_pool(device, 'n64_pool', '172.0.0.1', '172.0.0.100')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['nat64 v4 pool n64_pool 172.0.0.1 172.0.0.100'],)
        )