from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_mpls_bgp_forwarding
from unittest.mock import Mock


class TestUnconfigureMplsBgpForwarding(TestCase):

    def test_unconfigure_mpls_bgp_forwarding(self):
        self.device = Mock()
        result = unconfigure_mpls_bgp_forwarding(self.device, 'po10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface po10', 'no mpls bgp forwarding'],)
        )
