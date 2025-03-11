from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_dtls_trustpoint
from unittest.mock import Mock


class TestConfigureRadiusServerDtlsTrustpoint(TestCase):

    def test_configure_radius_server_dtls_trustpoint(self):
        self.device = Mock()
        result = configure_radius_server_dtls_trustpoint(self.device, 'TMP_NAME', 'tmp', 'client')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server TMP_NAME', 'dtls trustpoint server tmp', 'dtls trustpoint client client'],)
        )
