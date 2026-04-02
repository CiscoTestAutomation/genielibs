from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat_pool

class TestUnconfigureNatPool(TestCase):

    def test_unconfigure_nat_pool(self):
        device = Mock()
        result = unconfigure_nat_pool(device, 'outside_pool', '4.4.4.4', '4.5.5.5', '255.0.0.0', None)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat pool outside_pool 4.4.4.4 4.5.5.5 netmask 255.0.0.0',)
        )

    def test_unconfigure_nat_pool_1(self):
        device = Mock()
        result = unconfigure_nat_pool(device, 'outside_pool1', '4.4.4.4', '4.4.5.5', None, 16)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat pool outside_pool1 4.4.4.4 4.4.5.5 prefix-length 16',)
        )