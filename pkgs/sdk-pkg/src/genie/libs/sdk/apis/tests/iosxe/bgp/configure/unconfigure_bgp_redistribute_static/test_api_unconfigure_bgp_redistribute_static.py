from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_bgp_redistribute_static
from unittest.mock import Mock


class TestUnconfigureBgpRedistributeStatic(TestCase):

    def test_unconfigure_bgp_redistribute_static(self):
        self.device = Mock()
        result = unconfigure_bgp_redistribute_static(self.device, 65000, 'vpnv4', None, 'test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 65000', 'address-family vpnv4', 'no redistribute static route-map test'],)
        )
