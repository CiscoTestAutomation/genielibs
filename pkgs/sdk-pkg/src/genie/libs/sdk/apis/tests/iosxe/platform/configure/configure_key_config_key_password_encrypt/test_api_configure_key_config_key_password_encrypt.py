from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_key_config_key_password_encrypt


class TestConfigureKeyConfigKeyPasswordEncrypt(TestCase):

    def test_configure_key_config_key_password_encrypt(self):
        device = Mock()

        result = configure_key_config_key_password_encrypt(device, 'Secret12345')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['key config-key password encrypt Secret12345'],)
        )