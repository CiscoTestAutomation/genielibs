from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_sxp_list_option
from unittest.mock import Mock


class TestConfigureCtsSxpListOption(TestCase):

    def test_configure_cts_sxp_list_option(self):
        self.device = Mock()
        result = configure_cts_sxp_list_option(self.device, 'export-list', 'MY_LIST', 'vrf', 'VRF-GRP-1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts sxp export-list MY_LIST', 'vrf VRF-GRP-1'],)
        )
