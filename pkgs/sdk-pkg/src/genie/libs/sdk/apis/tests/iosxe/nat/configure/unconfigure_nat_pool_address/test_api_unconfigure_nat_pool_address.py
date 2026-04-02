from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat_pool_address

class TestUnconfigureNatPoolAddress(TestCase):

    def test_unconfigure_nat_pool_address(self):
        device = Mock()
        result = unconfigure_nat_pool_address(
            device, 'inside_pool1', '1.1.1.1', '1.2.2.2', '255.0.0.0', None, 'match-host'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'ip nat pool inside_pool1 netmask 255.0.0.0 type match-host',
                'no address 1.1.1.1 1.2.2.2'
            ],)
        )

    def test_unconfigure_nat_pool_address_1(self):
        device = Mock()
        result = unconfigure_nat_pool_address(
            device, 'inside_pool2', '1.1.1.1', '1.2.2.2', None, 8, None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'ip nat pool inside_pool2 prefix-length 8',
                'no address 1.1.1.1 1.2.2.2'
            ],)
        )