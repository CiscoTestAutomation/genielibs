from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_dtls_watchdoginterval
from unittest.mock import Mock


class TestConfigureRadiusServerDtlsWatchdoginterval(TestCase):

    def test_configure_radius_server_dtls_watchdoginterval(self):
        self.device = Mock()
        result = configure_radius_server_dtls_watchdoginterval(self.device, 'TMP_NAME', '2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server TMP_NAME', 'dtls watchdoginterval 2'],)
        )
