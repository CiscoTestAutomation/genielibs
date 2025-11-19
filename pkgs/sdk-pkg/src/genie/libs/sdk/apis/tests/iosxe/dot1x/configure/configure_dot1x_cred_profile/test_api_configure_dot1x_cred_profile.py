from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_dot1x_cred_profile
from unittest.mock import Mock


class TestConfigureDot1xCredProfile(TestCase):

    def test_configure_dot1x_cred_profile(self):
        self.device = Mock()
        result = configure_dot1x_cred_profile(self.device, 'dot1x_prof', 'dotxuser', ']hc[ZbOgC[X[_JV_cbCgIUbSAGK', 'ENCRYPTED')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (('dot1x credentials dot1x_prof\n'
 'username dotxuser\n'
 'password 6 ]hc[ZbOgC[X[_JV_cbCgIUbSAGK\n'),)
        )
