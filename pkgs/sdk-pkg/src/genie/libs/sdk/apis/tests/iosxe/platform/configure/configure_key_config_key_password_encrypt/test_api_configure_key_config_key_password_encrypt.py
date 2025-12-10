from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_key_config_key_password_encrypt
from unittest.mock import Mock


class TestConfigureKeyConfigKeyPasswordEncrypt(TestCase):

    def test_configure_key_config_key_password_encrypt(self):
        self.device = Mock()
        result = configure_key_config_key_password_encrypt(self.device, 'Secret12345')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['key config-key password encrypt Secret12345'],)
        )
