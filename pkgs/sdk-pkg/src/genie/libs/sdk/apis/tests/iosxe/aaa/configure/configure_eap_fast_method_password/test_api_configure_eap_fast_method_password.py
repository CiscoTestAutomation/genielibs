from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_eap_fast_method_password
from unittest.mock import Mock


class TestConfigureEapFastMethodPassword(TestCase):

    def test_configure_eap_fast_method_password(self):
        self.device = Mock()
        result = configure_eap_fast_method_password(self.device, 'EAP', ']hc[ZbOgC[X[_JV_cbCgIUbSAGK', '6', ']hc[ZbOgC[X[_JV_cbCgIUbSAGK', '6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['eap method fast profile EAP', 'local-key 6 ]hc[ZbOgC[X[_JV_cbCgIUbSAGK', 'pac-password 6 ]hc[ZbOgC[X[_JV_cbCgIUbSAGK'],)
        )
