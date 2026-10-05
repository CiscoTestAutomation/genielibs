from unittest import TestCase
from genie.libs.sdk.apis.iosxe.key.configure import unconfigure_key_config_key_password_encrypt
from unittest.mock import Mock


class TestUnconfigureKeyConfigKeyPasswordEncrypt(TestCase):

    def test_unconfigure_key_config_key_password_encrypt(self):
        self.device = Mock()
        result = unconfigure_key_config_key_password_encrypt(self.device, 'cisco123')
        self.assertEqual(result, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no key config-key password-encrypt',)
        )

    def test_unconfigure_key_config_key_password_encrypt_old_key(self):
        self.device = Mock()
        result = unconfigure_key_config_key_password_encrypt(self.device, old_key='cisco123')
        self.assertEqual(result, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no key config-key password-encrypt',)
        )

    def test_unconfigure_key_config_key_password_encrypt_mismatch(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_key_config_key_password_encrypt(
                self.device, password='cisco123', old_key='cisco456'
            )
