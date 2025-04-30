from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_dtls_port
from unittest.mock import Mock


class TestConfigureRadiusServerDtlsPort(TestCase):

    def test_configure_radius_server_dtls_port(self):
        self.device = Mock()
        result = configure_radius_server_dtls_port(self.device, 'TMP_NAME', '2083')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server TMP_NAME', 'dtls port 2083'],)
        )
