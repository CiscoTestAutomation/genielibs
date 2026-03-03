from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_pim_rp_address

class TestUnconfigureIpPimRpAddress(TestCase):

    def test_unconfigure_ip_pim_rp_address(self):
        device = Mock()
        result = unconfigure_ip_pim_rp_address(device, '1.1.1.1', 'bidir')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip pim rp-address 1.1.1.1 bidir',)
        )