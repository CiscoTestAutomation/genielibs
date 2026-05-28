import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_ip_tftp_blocksize


class TestUnconfigureIpTftpBlocksize(unittest.TestCase):

    def test_unconfigure_ip_tftp_blocksize(self):
        device = Mock()

        result = unconfigure_ip_tftp_blocksize(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip tftp blocksize',)
        )