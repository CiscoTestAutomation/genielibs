import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import disable_login_password_reuse_interval


class TestDisableLoginPasswordReuseInterval(unittest.TestCase):

    def test_disable_login_password_reuse_interval(self):
        self.device = Mock()
        disable_login_password_reuse_interval(self.device)
        self.device.configure.assert_called_once_with(
            "no login password-reuse-interval"
        )
