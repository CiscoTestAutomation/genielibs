from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_trustpoint
from unittest.mock import Mock


class TestConfigureTrustpoint(TestCase):

    def test_configure_trustpoint(self):
        self.device = Mock()
        result = configure_trustpoint(self.device, 'None', 'Self', 2048, False, None, False, None, None, None, None, None, None, None, False, None, None, None, False, False, None, False, False, False, None, None, None, False, 'selfsigned', None, False, False, False, None, None, None, None, None, None, None, None, None, False, False, None, None, False, False, None, None, None, False, None, None, None, None, None, 'cn=Self', None, None, None, None, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki trustpoint Self', 'revocation-check None', 'rsakeypair Self 2048', 'enrollment selfsigned', 'subject-name cn=Self'],)
        )
