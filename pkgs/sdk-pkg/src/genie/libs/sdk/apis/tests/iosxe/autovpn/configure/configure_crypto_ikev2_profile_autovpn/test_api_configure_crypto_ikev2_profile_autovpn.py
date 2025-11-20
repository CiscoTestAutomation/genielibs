from unittest import TestCase
from genie.libs.sdk.apis.iosxe.autovpn.configure import configure_crypto_ikev2_profile_autovpn
from unittest.mock import Mock


class TestConfigureCryptoIkev2ProfileAutovpn(TestCase):

    def test_configure_crypto_ikev2_profile_autovpn(self):
        self.device = Mock()
        result = configure_crypto_ikev2_profile_autovpn(self.device, 'autovpn_profile', 'autovpn', True, 'pre-share', 'pre-share', True, 1, 'autovpn_policy', 'autovpn_proposal')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 policy autovpn_policy', 'match app autovpn', 'proposal autovpn_proposal', 'crypto ikev2 profile autovpn_profile', 'match application autovpn', 'match identity remote any', 'authentication remote pre-share', 'authentication local pre-share', 'nat force-encap', 'virtual-template 1'],)
        )
