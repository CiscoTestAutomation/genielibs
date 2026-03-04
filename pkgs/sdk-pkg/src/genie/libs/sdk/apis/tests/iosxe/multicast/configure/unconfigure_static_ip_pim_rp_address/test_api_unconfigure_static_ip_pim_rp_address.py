from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_static_ip_pim_rp_address

class TestUnconfigureStaticIpPimRpAddress(TestCase):

    def test_unconfigure_static_ip_pim_rp_address(self):
        device = Mock()
        result = unconfigure_static_ip_pim_rp_address(device, '5.5.5.5', 'None')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip pim vrf None rp-address 5.5.5.5',)
        )