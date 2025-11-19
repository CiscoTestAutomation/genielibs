from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import configure_mpls_ldp_session_protection
from unittest.mock import Mock


class TestConfigureMplsLdpSessionProtection(TestCase):

    def test_configure_mpls_ldp_session_protection(self):
        self.device = Mock()
        result = configure_mpls_ldp_session_protection(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('mpls ldp session protection',)
        )
