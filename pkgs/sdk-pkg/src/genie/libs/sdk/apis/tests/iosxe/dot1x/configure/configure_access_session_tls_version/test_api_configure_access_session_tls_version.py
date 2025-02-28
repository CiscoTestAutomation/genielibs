from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_access_session_tls_version
from unittest.mock import Mock


class TestConfigureAccessSessionTlsVersion(TestCase):

    def test_configure_access_session_tls_version(self):
        self.device = Mock()
        result = configure_access_session_tls_version(self.device, 'all')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('access-session tls-version all',)
        )
