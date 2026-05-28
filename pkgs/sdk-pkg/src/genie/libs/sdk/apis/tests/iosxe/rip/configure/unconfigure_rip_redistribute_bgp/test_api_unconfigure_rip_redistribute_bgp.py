from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rip.configure import unconfigure_rip_redistribute_bgp
from unittest.mock import Mock


class TestUnconfigureRipRedistributeBgp(TestCase):

    def test_unconfigure_rip_redistribute_bgp(self):
        self.device = Mock()
        result = unconfigure_rip_redistribute_bgp(self.device, 200, 1, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router rip', 'no redistribute bgp 200 metric 1'],)
        )
