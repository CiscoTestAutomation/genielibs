from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_eap_fast_method_profile
from unittest.mock import Mock


class TestConfigureEapFastMethodProfile(TestCase):

    def test_configure_eap_fast_method_profile(self):
        self.device = Mock()
        result = configure_eap_fast_method_profile(self.device, 'EAP_PROG')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('eap method fast profile EAP_PROG',)
        )
