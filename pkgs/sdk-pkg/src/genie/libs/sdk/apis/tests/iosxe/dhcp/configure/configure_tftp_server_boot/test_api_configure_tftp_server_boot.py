from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_tftp_server_boot
from unittest.mock import Mock


class TestConfigureTftpServerBoot(TestCase):

    def test_configure_tftp_server_boot(self):
        self.device = Mock()
        result = configure_tftp_server_boot(self.device, 'flash:ztp_http_latest.py')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['tftp-server flash:ztp_http_latest.py'],)
        )
