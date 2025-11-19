from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_mpls_ldp_session_protection
from unittest.mock import Mock


class TestUnconfigureMplsLdpSessionProtection(TestCase):

    def test_unconfigure_mpls_ldp_session_protection(self):
        self.device = Mock()
        result = unconfigure_mpls_ldp_session_protection(self.device, 'vrf1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no mpls ldp session protection vrf vrf1',)
        )
