import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_dot1x_cred_profile_secure


class TestConfigureDot1xCredProfileSecure(TestCase):

    @patch('genie.libs.sdk.apis.iosxe.dot1x.configure.configure_enable_aes_encryption')
    def test_type6(self, mock_aes):
        """Verify Type 6 enables AES and configures dot1x credentials."""
        device = Mock()
        device.name = 'Router1'
        configure_dot1x_cred_profile_secure(
            device, profile_name='DOT1X_PROF',
            user_name='testuser', passwd='Secret123',
            master_key='MasterKey123', algorithm_type='type6'
        )
        mock_aes.assert_called_once_with(device, 'MasterKey123', None)
        self.assertEqual(
            device.configure.call_args[0][0],
            [
                'dot1x credentials DOT1X_PROF',
                'username testuser',
                'password Secret123',
            ]
        )

    def test_type9(self):
        """Verify Type 9 configures dot1x with scrypt password."""
        device = Mock()
        device.name = 'Router1'
        configure_dot1x_cred_profile_secure(
            device, profile_name='DOT1X_PROF',
            user_name='testuser', passwd='Secret123',
            algorithm_type='type9'
        )
        self.assertEqual(
            device.configure.call_args[0][0],
            [
                'dot1x credentials DOT1X_PROF',
                'username testuser',
                'password algorithm-type scrypt Secret123',
            ]
        )

    def test_invalid_algorithm_type(self):
        """Verify ValueError for invalid algorithm_type."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_dot1x_cred_profile_secure(
                device, profile_name='DOT1X_PROF',
                user_name='testuser', passwd='Secret123',
                algorithm_type='invalid'
            )

    def test_type6_without_master_key(self):
        """Verify ValueError when type6 used without master_key."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_dot1x_cred_profile_secure(
                device, profile_name='DOT1X_PROF',
                user_name='testuser', passwd='Secret123',
                algorithm_type='type6'
            )

    @patch('genie.libs.sdk.apis.iosxe.dot1x.configure.configure_enable_aes_encryption')
    def test_device_failure(self, mock_aes):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_dot1x_cred_profile_secure(
                device, profile_name='DOT1X_PROF',
                user_name='testuser', passwd='Secret123',
                master_key='MasterKey123', algorithm_type='type6'
            )


if __name__ == '__main__':
    unittest.main()
