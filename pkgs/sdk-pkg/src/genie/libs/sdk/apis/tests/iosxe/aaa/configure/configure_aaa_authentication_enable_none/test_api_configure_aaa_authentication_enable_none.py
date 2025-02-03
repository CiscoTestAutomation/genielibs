from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authentication_enable_none
from unittest.mock import Mock


class TestConfigureAaaAuthenticationEnableNone(TestCase):

    def test_configure_aaa_authentication_enable_none(self):
        self.device = Mock()
        result = configure_aaa_authentication_enable_none(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authentication enable default none',)
        )
