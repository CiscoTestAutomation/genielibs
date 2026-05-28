import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_sftp_username


class TestConfigureIpSftpUsername(unittest.TestCase):

    def test_configure_ip_sftp_username(self):
        device = Mock()

        result = configure_ip_sftp_username(device, 'root')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip sftp username root',)
        )