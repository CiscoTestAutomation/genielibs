from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_tftp_server
from unittest.mock import Mock


class TestConfigureTftpServer(TestCase):

    def test_configure_tftp_server(self):
        self.device = Mock()
        result = configure_tftp_server(self.device, 'flash:', 'base2.cfg')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['tftp-server flash:base2.cfg'],)
        )
