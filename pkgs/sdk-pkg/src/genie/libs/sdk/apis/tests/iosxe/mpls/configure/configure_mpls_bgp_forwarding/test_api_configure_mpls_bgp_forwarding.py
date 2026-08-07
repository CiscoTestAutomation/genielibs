from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import configure_mpls_bgp_forwarding
from unittest.mock import Mock


class TestConfigureMplsBgpForwarding(TestCase):

    def test_configure_mpls_bgp_forwarding(self):
        self.device = Mock()
        result = configure_mpls_bgp_forwarding(self.device, 'po10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface po10', 'mpls bgp forwarding'],)
        )
