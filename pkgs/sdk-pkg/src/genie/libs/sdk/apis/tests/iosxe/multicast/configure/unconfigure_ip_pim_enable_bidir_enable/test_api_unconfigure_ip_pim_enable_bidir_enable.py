from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_pim_enable_bidir_enable

class TestUnconfigureIpPimEnableBidirEnable(TestCase):

    def test_unconfigure_ip_pim_enable_bidir_enable(self):
        device = Mock()
        result = unconfigure_ip_pim_enable_bidir_enable(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip pim bidir-enable',)
        )