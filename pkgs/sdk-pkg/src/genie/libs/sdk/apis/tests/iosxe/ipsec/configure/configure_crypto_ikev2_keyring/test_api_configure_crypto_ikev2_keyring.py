from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_crypto_ikev2_keyring
from unittest.mock import Mock


class TestConfigureCryptoIkev2Keyring(TestCase):

    def test_configure_crypto_ikev2_keyring(self):
        self.device = Mock()
        result = configure_crypto_ikev2_keyring(self.device, 'key1', 'peer1', 'test', '1.1.1.1', '255.255.255.0', 'ipv4', '1.1.1.1', '234', 'test1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 keyring key1', 'peer peer1', 'address 1.1.1.1 255.255.255.0', 'pre-shared-key test', 'identity address 1.1.1.1', 'ppk manual id 234 key test1'],)
        )
