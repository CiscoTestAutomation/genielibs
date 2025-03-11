from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mcast.configure import configure_pim_auto_rp_listener
from unittest.mock import Mock


class TestConfigurePimAutoRpListener(TestCase):

    def test_configure_pim_auto_rp_listener(self):
        self.device = Mock()
        result = configure_pim_auto_rp_listener(self.device, '0', '10', True, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip pim autorp listener', 'ip pim  send-rp-announce loopback 0 scope 10', 'ip pim  send-rp-discovery loopback 0 scope 10'],)
        )
