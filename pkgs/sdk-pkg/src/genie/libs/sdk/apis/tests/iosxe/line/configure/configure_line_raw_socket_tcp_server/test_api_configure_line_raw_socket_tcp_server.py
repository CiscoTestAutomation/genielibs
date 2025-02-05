from unittest import TestCase
from genie.libs.sdk.apis.iosxe.line.configure import configure_line_raw_socket_tcp_server
from unittest.mock import Mock


class TestConfigureLineRawSocketTcpServer(TestCase):

    def test_configure_line_raw_socket_tcp_server(self):
        self.device = Mock()
        result = configure_line_raw_socket_tcp_server(self.device, '0/3/0', '5.5.5.1', 5000)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line 0/3/0', 'raw-socket tcp server 5000 5.5.5.1'],)
        )
