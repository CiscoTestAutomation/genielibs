import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_ip_sftp_password


class TestUnconfigureIpSftpPassword(unittest.TestCase):

    def test_unconfigure_ip_sftp_password(self):
        device = Mock()

        result = unconfigure_ip_sftp_password(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip sftp password',)
        )