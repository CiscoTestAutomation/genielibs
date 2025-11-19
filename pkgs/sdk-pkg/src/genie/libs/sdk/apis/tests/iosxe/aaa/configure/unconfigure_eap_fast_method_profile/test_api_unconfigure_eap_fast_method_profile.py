from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_eap_fast_method_profile
from unittest.mock import Mock


class TestUnconfigureEapFastMethodProfile(TestCase):

    def test_unconfigure_eap_fast_method_profile(self):
        self.device = Mock()
        result = unconfigure_eap_fast_method_profile(self.device, 'EAP_PROG')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no eap method fast profile EAP_PROG',)
        )
