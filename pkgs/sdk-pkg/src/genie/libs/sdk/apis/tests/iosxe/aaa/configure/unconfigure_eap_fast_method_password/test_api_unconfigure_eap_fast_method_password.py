from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_eap_fast_method_password
from unittest.mock import Mock


class TestUnconfigureEapFastMethodPassword(TestCase):

    def test_unconfigure_eap_fast_method_password(self):
        self.device = Mock()
        result = unconfigure_eap_fast_method_password(self.device, 'EAP', ']hc[ZbOgC[X[_JV_cbCgIUbSAGK', '6', ']hc[ZbOgC[X[_JV_cbCgIUbSAGK', '6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['eap method fast profile EAP', 'no local-key 6 ]hc[ZbOgC[X[_JV_cbCgIUbSAGK', 'no pac-password 6 ]hc[ZbOgC[X[_JV_cbCgIUbSAGK'],)
        )