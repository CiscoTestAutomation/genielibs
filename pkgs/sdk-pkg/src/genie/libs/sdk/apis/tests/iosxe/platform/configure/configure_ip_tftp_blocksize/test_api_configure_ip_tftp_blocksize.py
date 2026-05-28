import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_tftp_blocksize


class TestConfigureIpTftpBlocksize(unittest.TestCase):

    def test_configure_ip_tftp_blocksize(self):
        device = Mock()

        result = configure_ip_tftp_blocksize(device, '2000')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip tftp blocksize 2000',)
        )