from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_pim_ssm

class TestUnconfigureIpPimSsm(TestCase):

    def test_unconfigure_ip_pim_ssm(self):
        device = Mock()
        result = unconfigure_ip_pim_ssm(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip pim ssm',)
        )