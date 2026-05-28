import unittest
from unittest.mock import Mock, patch
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.platform.configure import configure_secure_file_transfer


class TestConfigureSecureFileTransfer(unittest.TestCase):

    def test_configure_secure_file_transfer_default(self):
        """Verify configure_secure_file_transfer calls SSH/SCP APIs with default ssh_version='2'."""
        device = Mock()
        device.name = 'Switch1'
        with patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_ssh_version'
        ) as mock_ssh_ver, patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_ssh_source_interface'
        ) as mock_ssh_src, patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_scp_server_enable'
        ) as mock_scp:
            result = configure_secure_file_transfer(device, interface='Loopback0')
            self.assertIsNone(result)
            mock_ssh_ver.assert_called_once_with(device, '2')
            mock_ssh_src.assert_called_once_with(device, 'Loopback0')
            mock_scp.assert_called_once_with(device)

    def test_configure_secure_file_transfer_custom_version(self):
        """Verify configure_secure_file_transfer passes custom ssh_version."""
        device = Mock()
        device.name = 'Switch1'
        with patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_ssh_version'
        ) as mock_ssh_ver, patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_ssh_source_interface'
        ) as mock_ssh_src, patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_scp_server_enable'
        ) as mock_scp:
            configure_secure_file_transfer(device, interface='GigabitEthernet0/0', ssh_version='2')
            mock_ssh_ver.assert_called_once_with(device, '2')
            mock_ssh_src.assert_called_once_with(device, 'GigabitEthernet0/0')
            mock_scp.assert_called_once_with(device)

    def test_configure_secure_file_transfer_failure(self):
        """Verify SubCommandFailure is raised when an inner API fails."""
        device = Mock()
        device.name = 'Switch1'
        with patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_ssh_version',
            side_effect=SubCommandFailure('mock error')
        ), patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_ssh_source_interface'
        ), patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.configure_ip_scp_server_enable'
        ):
            with self.assertRaises(SubCommandFailure):
                configure_secure_file_transfer(device, interface='Loopback0')


if __name__ == '__main__':
    unittest.main()
