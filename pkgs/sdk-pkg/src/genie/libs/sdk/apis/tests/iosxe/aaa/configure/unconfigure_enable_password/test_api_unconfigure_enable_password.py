import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_enable_password


class TestUnconfigureEnablePassword(unittest.TestCase):

    def test_unconfigure_enable_password(self):
        self.device = Mock()
        unconfigure_enable_password(self.device, False, None)
        self.device.configure.assert_called_with(
            'no enable password'
        )

    def test_unconfigure_enable_password_1(self):
        self.device = Mock()
        unconfigure_enable_password(self.device, False, 15)
        self.device.configure.assert_called_with(
            'no enable password level 15'
        )

    def test_unconfigure_enable_password_2(self):
        self.device = Mock()
        unconfigure_enable_password(self.device, True, 15)
        self.device.configure.assert_called_with(
            'no enable secret level 15'
        )
            
