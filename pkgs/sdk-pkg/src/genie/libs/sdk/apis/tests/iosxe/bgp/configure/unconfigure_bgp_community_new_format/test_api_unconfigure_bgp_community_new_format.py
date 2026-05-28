from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_bgp_community_new_format
from unittest.mock import Mock


class TestUnconfigureBgpCommunityNewFormat(TestCase):

    def test_unconfigure_bgp_community_new_format(self):
        self.device = Mock()
        result = unconfigure_bgp_community_new_format(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip bgp-community new-format'],)
        )
