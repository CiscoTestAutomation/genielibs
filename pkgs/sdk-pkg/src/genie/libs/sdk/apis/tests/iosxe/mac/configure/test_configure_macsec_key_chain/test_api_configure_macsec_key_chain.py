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

    def test_configure_macsec_key_chain_with_mka_policy(self):
        """Test keychain + MKA policy configured from within keychain context
        (ACE/Cat9K platforms where 'mka policy' is invalid at global config).
        """
        self.device = Mock()

        keychain_name = 'k10'
        key = '01'
        key_string = '12345678123456781234567812345678'
        mka_policy_name = 'abc'
        mka_cipher = 'gcm-aes-128'
        key_server_priority = '10'

        configure_macsec_key_chain(
            self.device,
            keychain_name=keychain_name,
            key=key,
            key_string=key_string,
            mka_policy_name=mka_policy_name,
            mka_cipher=mka_cipher,
            key_server_priority=key_server_priority,
        )

        expected_commands = [
            f"key chain {keychain_name} macsec",
            f"key {key}",
            f"key-string {key_string}",
            "exit",
            f"mka policy {mka_policy_name}",
            f"macsec {mka_cipher}",
            f"key-server priority {key_server_priority}",
        ]

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_commands,)
        )
