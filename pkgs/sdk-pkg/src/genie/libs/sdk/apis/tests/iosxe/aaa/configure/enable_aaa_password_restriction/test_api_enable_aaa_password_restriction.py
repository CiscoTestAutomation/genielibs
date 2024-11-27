import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import enable_aaa_password_restriction


class TestEnableAaaPasswordRestriction(unittest.TestCase):

    def test_enable_aaa_password_restriction(self):
        self.device = Mock()
        enable_aaa_password_restriction(self.device)
        self.device.configure.assert_called_once_with(
            "aaa password restriction"
        )
