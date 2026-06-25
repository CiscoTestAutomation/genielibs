import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_username_secure


class TestConfigureUsernameSecure(TestCase):

    @patch('genie.libs.sdk.apis.iosxe.aaa.configure.configure_enable_aes_encryption')
    def test_type6_with_username(self, mock_aes):
        """Verify Type 6 configures username secret after enabling AES."""
        device = Mock()
        device.name = 'Router1'
        configure_username_secure(
            device, master_key='MasterKey123',
            username='admin', pwd='Secret123',
            algorithm_type='type6'
        )
        mock_aes.assert_called_once_with(device, 'MasterKey123', None)
        self.assertEqual(
            device.configure.call_args[0][0],
            ['username admin secret Secret123']
        )

    @patch('genie.libs.sdk.apis.iosxe.aaa.configure.configure_enable_aes_encryption')
    def test_type6_with_enable_secret(self, mock_aes):
        """Verify Type 6 configures enable secret."""
        device = Mock()
        device.name = 'Router1'
        configure_username_secure(
            device, master_key='MasterKey123',
            enable_secret='EnablePass',
            algorithm_type='type6'
        )
        mock_aes.assert_called_once()
        self.assertEqual(
            device.configure.call_args[0][0],
            ['enable secret EnablePass']
        )

    def test_type9_with_username(self):
        """Verify Type 9 configures username with scrypt."""
        device = Mock()
        device.name = 'Router1'
        configure_username_secure(
            device, username='admin', pwd='Secret123',
            algorithm_type='type9'
        )
        # First call removes existing password, second call configures new
        self.assertIn(
            'username admin algorithm-type scrypt secret Secret123',
            device.configure.call_args[0][0]
        )

    def test_invalid_algorithm_type(self):
        """Verify ValueError for invalid algorithm_type."""
        device = Mock()
        device.name = 'Router1'
        with self.assertRaises(ValueError):
            configure_username_secure(
                device, username='admin', pwd='Secret123',
                algorithm_type='invalid'
            )

    def test_username_without_pwd(self):
        """Verify ValueError when username provided without pwd."""
        device = Mock()
        device.name = 'Router1'
        with self.assertRaises(ValueError):
            configure_username_secure(
                device, username='admin', algorithm_type='type9'
            )

    def test_type6_without_master_key(self):
        """Verify ValueError when type6 used without master_key."""
        device = Mock()
        device.name = 'Router1'
        with self.assertRaises(ValueError):
            configure_username_secure(
                device, username='admin', pwd='Secret123',
                algorithm_type='type6'
            )

    @patch('genie.libs.sdk.apis.iosxe.aaa.configure.configure_enable_aes_encryption')
    def test_device_failure(self, mock_aes):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_username_secure(
                device, master_key='MasterKey123',
                username='admin', pwd='Secret123',
                algorithm_type='type6'
            )


if __name__ == '__main__':
    unittest.main()
