from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_raw_socket_client
from unittest.mock import Mock


class TestConfigureInterfaceRawSocketClient(TestCase):

    def test_configure_interface_raw_socket_client(self):
        self.device = Mock()
        result = configure_interface_raw_socket_client(self.device, 'loopback 55', '5.5.5.1', 5000, '5.5.5.7', 6000)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface loopback 55', 'raw-socket tcp client 5.5.5.1 5000 5.5.5.7 6000'],)
        )
