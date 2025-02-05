from unittest import TestCase
from genie.libs.sdk.apis.iosxe.line.configure import configure_line_raw_socket_tcp_client
from unittest.mock import Mock


class TestConfigureLineRawSocketTcpClient(TestCase):

    def test_configure_line_raw_socket_tcp_client(self):
        self.device = Mock()
        result = configure_line_raw_socket_tcp_client(self.device, '0/3/0', '5.5.5.1', 5000, '5.5.5.2', 6000)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line 0/3/0', 'raw-socket tcp client 5.5.5.1 5000 5.5.5.2 6000'],)
        )
