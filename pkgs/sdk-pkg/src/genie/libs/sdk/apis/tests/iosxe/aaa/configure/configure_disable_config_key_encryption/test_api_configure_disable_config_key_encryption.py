import unittest
from unittest.mock import Mock, patch
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_disable_config_key_encryption


class TestConfigureDisableConfigKeyEncryption(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_disable_config_key_encryption(self):
        with patch('genie.libs.sdk.apis.iosxe.aaa.configure.Dialog') as mock_dialog:
            configure_disable_config_key_encryption(self.device)
        self.device.configure.assert_called_once_with(
            'no key config-key password-encrypt',
            reply=mock_dialog()
        )
