from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authentication_ppp_default_type
from unittest.mock import Mock


class TestConfigureAaaAuthenticationPppDefaultType(TestCase):

    def test_configure_aaa_authentication_ppp_default_type(self):
        self.device = Mock()
        result = configure_aaa_authentication_ppp_default_type(self.device, 'local')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authentication ppp default local',)
        )
