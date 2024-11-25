import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import enable_login_password_reuse_interval


class TestEnableLoginPasswordReuseInterval(unittest.TestCase):

    def test_enable_login_password_reuse_interval(self):
        self.device = Mock()
        enable_login_password_reuse_interval(self.device, 250)
        self.device.configure.assert_called_once_with(
            "login password-reuse-interval 250"
        )
