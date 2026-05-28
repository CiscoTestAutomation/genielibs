from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.configure import configure_macsec_key_chain


class TestConfigureMacsecKeyChain(TestCase):

    def test_configure_macsec_key_chain(self):
        self.device = Mock()

        keychain_name = 'KC_MACSEC'
        key = 42
        key_string = 'MySecretKey123'

        configure_macsec_key_chain(
            self.device,
            keychain_name=keychain_name,
            key=key,
            key_string=key_string
        )

        expected_commands = [
            f"key chain {keychain_name} macsec",
            f"key {key}",
            f"key-string {key_string}",
            "exit",
        ]

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_commands,)
        )
