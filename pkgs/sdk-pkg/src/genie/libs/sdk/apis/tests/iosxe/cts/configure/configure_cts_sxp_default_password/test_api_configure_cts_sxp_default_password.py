from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_sxp_default_password
from unittest.mock import Mock


class TestConfigureCtsSxpDefaultPassword(TestCase):

    def test_configure_cts_sxp_default_password(self):
        self.device = Mock()
        result = configure_cts_sxp_default_password(self.device, 'cisco')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts sxp default password cisco'],)
        )
