from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_key_config_key_password_encrypt
from unittest.mock import Mock


class TestUnconfigureKeyConfigKeyPasswordEncrypt(TestCase):

    def test_unconfigure_key_config_key_password_encrypt(self):
        self.device = Mock()
        result = unconfigure_key_config_key_password_encrypt(self.device, 'Secret12345')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no key config-key password encrypt Secret12345'],)
        )
