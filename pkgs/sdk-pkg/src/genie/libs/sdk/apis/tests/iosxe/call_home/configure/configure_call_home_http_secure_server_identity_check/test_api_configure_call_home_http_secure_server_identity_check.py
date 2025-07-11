from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_http_secure_server_identity_check


class TestConfigureCallHomeHttpSecureServerIdentityCheck(TestCase):

    def test_configure_call_home_http_secure_server_identity_check(self):
        self.device = Mock()
        result = configure_call_home_http_secure_server_identity_check(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'http secure server-identity-check'],)
        )
