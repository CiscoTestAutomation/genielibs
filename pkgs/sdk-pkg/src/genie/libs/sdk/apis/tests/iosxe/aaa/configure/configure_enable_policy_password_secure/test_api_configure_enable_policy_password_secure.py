import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_enable_policy_password_secure


class TestConfigureEnablePolicyPasswordSecure(TestCase):

    @patch('genie.libs.sdk.apis.iosxe.aaa.configure.configure_enable_aes_encryption')
    def test_type6(self, mock_aes):
        """Verify Type 6 enables AES and configures enable password."""
        device = Mock()
        device.name = 'Router1'
        configure_enable_policy_password_secure(
            device, password='Secret123', master_key='MasterKey123',
            algorithm_type='type6'
        )
        mock_aes.assert_called_once_with(device, 'MasterKey123', None)
        self.assertIn('enable password Secret123', device.configure.call_args[0][0])

    def test_type9(self):
        """Verify Type 9 configures enable with scrypt."""
        device = Mock()
        device.name = 'Router1'
        configure_enable_policy_password_secure(
            device, password='Secret123', algorithm_type='type9'
        )
        self.assertIn(
            'enable algorithm-type scrypt secret Secret123',
            device.configure.call_args[0][0]
        )

    def test_invalid_algorithm_type(self):
        """Verify ValueError for invalid algorithm_type."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_enable_policy_password_secure(
                device, password='Secret123', algorithm_type='invalid'
            )

    def test_type6_without_master_key(self):
        """Verify ValueError when type6 used without master_key."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_enable_policy_password_secure(
                device, password='Secret123', algorithm_type='type6'
            )

    @patch('genie.libs.sdk.apis.iosxe.aaa.configure.configure_enable_aes_encryption')
    def test_device_failure(self, mock_aes):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_enable_policy_password_secure(
                device, password='Secret123', master_key='MasterKey123',
                algorithm_type='type6'
            )


if __name__ == '__main__':
    unittest.main()
