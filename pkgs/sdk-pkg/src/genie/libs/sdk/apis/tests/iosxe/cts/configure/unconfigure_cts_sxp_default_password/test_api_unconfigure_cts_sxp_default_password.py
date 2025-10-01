from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_sxp_default_password
from unittest.mock import Mock


class TestUnconfigureCtsSxpDefaultPassword(TestCase):

    def test_unconfigure_cts_sxp_default_password(self):
        self.device = Mock()
        result = unconfigure_cts_sxp_default_password(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sxp default password'],)
        )
