import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_service_password_encryption


class TestUnconfigureServicePasswordEncryption(unittest.TestCase):

    def test_unconfigure_service_password_encryption(self):
        self.device = Mock()
        unconfigure_service_password_encryption(device=self.device)
        self.device.configure.assert_called_with(
            'no service password-encryption'
        )