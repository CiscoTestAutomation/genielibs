import unittest
from genie.libs.sdk.apis.iosxe.aaa.configure import disable_aaa_password_restriction
from unittest.mock import Mock

class TestDisableAaaPasswordRestriction(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_disable_aaa_password_restriction(self):
        disable_aaa_password_restriction(self.device)
        self.device.configure.assert_called_once_with(
            'no aaa password restriction'
        )
