from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import unconfigure_access_session_tls_version
from unittest.mock import Mock


class TestUnconfigureAccessSessionTlsVersion(TestCase):

    def test_unconfigure_access_session_tls_version(self):
        self.device = Mock()
        result = unconfigure_access_session_tls_version(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no access-session tls-version',)
        )
