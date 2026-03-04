from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_pim_vrf_ssm_default

class TestUnconfigureIpPimVrfSsmDefault(TestCase):

    def test_unconfigure_ip_pim_vrf_ssm_default(self):
        device = Mock()
        result = unconfigure_ip_pim_vrf_ssm_default(device, 'vrf3001')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip pim vrf vrf3001 ssm default',)
        )