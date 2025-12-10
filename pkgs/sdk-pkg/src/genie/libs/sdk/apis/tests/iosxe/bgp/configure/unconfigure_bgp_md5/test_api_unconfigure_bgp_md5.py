from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_bgp_md5
from unittest.mock import Mock


class TestUnconfigureBgpMd5(TestCase):

    def test_unconfigure_bgp_md5(self):
        self.device = Mock()
        result = unconfigure_bgp_md5(self.device, 65002, '13.1.0.1', 'cisco123', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 65002', 'no neighbor 13.1.0.1 password cisco123'],)
        )
