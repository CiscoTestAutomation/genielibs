import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_enable_policy_password


class TestUnconfigureEnablePolicyPassword(unittest.TestCase):

    def test_unconfigure_enable_policy_password(self):
        self.device = Mock()
        unconfigure_enable_policy_password(device=self.device, password='Test12', policy_name=None, password_type=None)
        self.device.configure.assert_called_with(
            'no enable password Test12'
        )

    def test_unconfigure_enable_policy_password_1(self):
        self.device = Mock()
        unconfigure_enable_policy_password(device=self.device, password='Test12', policy_name='enable_test', password_type=0)
        self.device.configure.assert_called_with(
            'no enable common-criteria-policy enable_test password 0 Test12'
        )
