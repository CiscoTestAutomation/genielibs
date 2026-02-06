from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_sxp_list_option
from unittest.mock import Mock


class TestUnconfigureCtsSxpListOption(TestCase):

    def test_unconfigure_cts_sxp_list_option(self):
        self.device = Mock()
        result = unconfigure_cts_sxp_list_option(self.device, 'export-list', 'MY_LIST')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sxp export-list MY_LIST'],)
        )
