from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_dtls_connection
from unittest.mock import Mock


class TestConfigureRadiusServerDtlsConnection(TestCase):

    def test_configure_radius_server_dtls_connection(self):
        self.device = Mock()
        result = configure_radius_server_dtls_connection(self.device, 'TMP_NAME', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server TMP_NAME', 'dtls connectiontimeout 1', 'exit'],)
        )
