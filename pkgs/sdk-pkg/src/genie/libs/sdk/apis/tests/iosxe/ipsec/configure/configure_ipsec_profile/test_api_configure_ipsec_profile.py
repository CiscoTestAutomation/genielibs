from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_profile
from unittest.mock import Mock


class TestConfigureIpsecProfile(TestCase):

    def test_configure_ipsec_profile(self):
        self.device = Mock()
        result = configure_ipsec_profile(self.device, 'dmvpn-hub', 'tset1', 'ikev2profile', None, False, False, False, False, False, False, None, False, None, False, None, None, False, None, None, False, 'group21', None, None, None, None, None, False, None, False, None, 'mlkem1024')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ipsec profile dmvpn-hub', 'set transform-set tset1', 'set ikev2-profile ikev2profile', 'set pfs group21 pqc mlkem1024'],)
        )
