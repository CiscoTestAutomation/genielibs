from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_tftp_server
from unittest.mock import Mock


class TestUnconfigureTftpServer(TestCase):

    def test_unconfigure_tftp_server(self):
        self.device = Mock()
        result = unconfigure_tftp_server(self.device, 'flash:', 'base2.cfg')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no tftp-server flash:base2.cfg'],)
        )
