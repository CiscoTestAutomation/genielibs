from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_bgp_redistribute_internal
from unittest.mock import Mock


class TestUnconfigureBgpRedistributeInternal(TestCase):

    def test_unconfigure_bgp_redistribute_internal(self):
        self.device = Mock()
        result = unconfigure_bgp_redistribute_internal(self.device, '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 1', 'no bgp redistribute-internal'],)
        )
