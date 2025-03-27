from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_with_dtls
from unittest.mock import Mock


class TestConfigureRadiusServerWithDtls(TestCase):

    def test_configure_radius_server_with_dtls(self):
        self.device = Mock()
        result = configure_radius_server_with_dtls(self.device, 'TMP_NAME', 'False')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server TMP_NAME', 'dtls', 'exit'],)
        )
