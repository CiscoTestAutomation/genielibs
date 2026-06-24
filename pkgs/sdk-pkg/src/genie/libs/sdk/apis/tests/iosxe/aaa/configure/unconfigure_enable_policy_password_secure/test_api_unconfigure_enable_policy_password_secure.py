import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_enable_policy_password_secure


class TestUnconfigureEnablePolicyPasswordSecure(TestCase):

    def test_unconfigure_with_password(self):
        """Verify 'no enable password <pwd>' is sent."""
        device = Mock()
        device.name = 'Router1'
        unconfigure_enable_policy_password_secure(device, password='Secret123')
        self.assertIn(
            'no enable password Secret123',
            device.configure.call_args[0][0]
        )

    def test_unconfigure_empty_password(self):
        """Verify 'no enable password' is sent when password is empty."""
        device = Mock()
        device.name = 'Router1'
        unconfigure_enable_policy_password_secure(device, password='')
        self.assertIn(
            'no enable password',
            device.configure.call_args[0][0]
        )

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_enable_policy_password_secure(device, password='Secret123')


if __name__ == '__main__':
    unittest.main()
