from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import configure_simulator_radius_server


class TestConfigureSimulatorRadiusServer(TestCase):

    def test_configure_simulator_radius_server_all_options(self):
        self.device = Mock()
        configure_simulator_radius_server(
            self.device, '10.1.1.1',
            user_prefixes=[
                {'prefix': 'aaaa', 'subscriber': 8},
                {'prefix': 'client1', 'subscriber': 8},
                {'prefix': 'service1', 'subscriber': 13},
            ],
            client_ip='10.2.2.2', shared_secret='cisco123'
        )
        self.device.configure.assert_called_once_with(
            [
                "simulator radius server 10.1.1.1",
                " user-name prefix aaaa subscriber 8",
                " user-name prefix client1 subscriber 8",
                " user-name prefix service1 subscriber 13",
                " client 10.2.2.2 shared-secret cisco123",
            ]
        )

    def test_configure_simulator_radius_server_no_client(self):
        self.device = Mock()
        configure_simulator_radius_server(
            self.device, '10.1.1.1',
            user_prefixes=[
                {'prefix': 'aaaa', 'subscriber': 8},
            ]
        )
        self.device.configure.assert_called_once_with(
            [
                "simulator radius server 10.1.1.1",
                " user-name prefix aaaa subscriber 8",
            ]
        )

    def test_configure_simulator_radius_server_remove_prefix(self):
        self.device = Mock()
        configure_simulator_radius_server(
            self.device, '10.1.1.1',
            user_prefixes=[
                {'prefix': 'client1', 'subscriber': 8},
            ],
            remove_prefixes=['aaaa']
        )
        self.device.configure.assert_called_once_with(
            [
                "simulator radius server 10.1.1.1",
                " no user-name prefix aaaa",
                " user-name prefix client1 subscriber 8",
            ]
        )
