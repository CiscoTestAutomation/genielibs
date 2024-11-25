import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_service_password_encryption


class TestConfigureServicePasswordEncryption(unittest.TestCase):

    def test_configure_service_password_encryption(self):
        self.device = Mock()
        configure_service_password_encryption(device=self.device)
        self.device.configure.assert_called_once_with(
            "service password-encryption"
        )
