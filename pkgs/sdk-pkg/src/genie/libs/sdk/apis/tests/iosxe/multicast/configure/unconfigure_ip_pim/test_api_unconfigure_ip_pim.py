from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_pim

class TestUnconfigureIpPim(TestCase):

    def test_unconfigure_ip_pim(self):
        device = Mock()
        result = unconfigure_ip_pim(device, 'TwentyFiveGigE1/0/2', 'sparse-mode')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE1/0/2', 'no ip pim sparse-mode'],)
        )