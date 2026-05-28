import unittest
from unittest.mock import Mock, patch
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_secure_file_transfer


class TestUnconfigureSecureFileTransfer(unittest.TestCase):

    def test_unconfigure_secure_file_transfer_default(self):
        """Verify unconfigure_secure_file_transfer calls unconfigure APIs."""
        device = Mock()
        device.name = 'Switch1'
        with patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.unconfigure_ip_scp_server_enable'
        ) as mock_unscp, patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.unconfigure_ip_ssh_source_interface'
        ) as mock_unssh:
            result = unconfigure_secure_file_transfer(device)
            self.assertIsNone(result)
            mock_unscp.assert_called_once_with(device)
            mock_unssh.assert_called_once_with(device)

    def test_unconfigure_secure_file_transfer_failure(self):
        """Verify SubCommandFailure is raised when an inner API fails."""
        device = Mock()
        device.name = 'Switch1'
        with patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.unconfigure_ip_scp_server_enable',
            side_effect=SubCommandFailure('mock error')
        ), patch(
            'genie.libs.sdk.apis.iosxe.platform.configure.unconfigure_ip_ssh_source_interface'
        ):
            with self.assertRaises(SubCommandFailure):
                unconfigure_secure_file_transfer(device)


if __name__ == '__main__':
    unittest.main()
