from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mcast.configure import unconfigure_pim_auto_rp_listener
from unittest.mock import Mock


class TestUnconfigurePimAutoRpListener(TestCase):

    def test_unconfigure_pim_auto_rp_listener(self):
        self.device = Mock()
        result = unconfigure_pim_auto_rp_listener(self.device, '0', '10', True, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip pim autorp listener', 'no ip pim send-rp-discovery loopback 0 scope 10', 'no ip pim send-rp-announce loopback 0 scope 10'],)
        )
