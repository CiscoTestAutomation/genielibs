from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_pool

class TestConfigureNatPool(TestCase):

    def test_configure_nat_pool(self):
        device = Mock()
        result = configure_nat_pool(device, 'outside_pool', '4.4.4.4', '4.5.5.5', '255.0.0.0', None)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip nat pool outside_pool 4.4.4.4 4.5.5.5 netmask 255.0.0.0'],)
        )

    def test_configure_nat_pool_1(self):
        device = Mock()
        result = configure_nat_pool(device, 'outside_pool1', '4.4.4.4', '4.5.5.5', None, 8)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip nat pool outside_pool1 4.4.4.4 4.5.5.5 prefix-length 8'],)
        )