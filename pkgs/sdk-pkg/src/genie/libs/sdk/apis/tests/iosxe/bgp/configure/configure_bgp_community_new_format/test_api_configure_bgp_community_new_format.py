from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_community_new_format
from unittest.mock import Mock


class TestConfigureBgpCommunityNewFormat(TestCase):

    def test_configure_bgp_community_new_format(self):
        self.device = Mock()
        result = configure_bgp_community_new_format(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip bgp-community new-format'],)
        )
