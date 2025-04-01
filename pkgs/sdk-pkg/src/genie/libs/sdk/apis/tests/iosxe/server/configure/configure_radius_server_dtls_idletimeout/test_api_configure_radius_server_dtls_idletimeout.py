from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_dtls_idletimeout
from unittest.mock import Mock


class TestConfigureRadiusServerDtlsIdletimeout(TestCase):

    def test_configure_radius_server_dtls_idletimeout(self):
        self.device = Mock()
        result = configure_radius_server_dtls_idletimeout(self.device, 'TMP_NAME', '60')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server TMP_NAME'],)
        )
