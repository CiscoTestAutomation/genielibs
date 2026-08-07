from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import (
    configure_simulator_radius_client_host,
)


class TestConfigureSimulatorRadiusClientHost(TestCase):

    def test_configure_simulator_radius_client_host(self):
        self.device = Mock()
        configure_simulator_radius_client_host(
            self.device,
            "10.1.1.1",
            "1645 1645",
            "1646 1646",
            "10.2.2.2",
            "1645",
            "1646",
            key="cisco",
            key_type="0",
        )
        self.device.configure.assert_called_once_with(
            [
                "simulator radius client 10.1.1.1 access-ports 1645 1645"
                " accounting-ports 1646 1646",
                "simulator radius host 10.2.2.2 auth-port 1645 acct-port 1646"
                " key 0 cisco",
            ]
        )

    def test_configure_simulator_radius_client_host_no_key(self):
        self.device = Mock()
        configure_simulator_radius_client_host(
            self.device,
            "10.1.1.1",
            "1645 1645",
            "1646 1646",
            "10.2.2.2",
            "1645",
            "1646",
        )
        self.device.configure.assert_called_once_with(
            [
                "simulator radius client 10.1.1.1 access-ports 1645 1645"
                " accounting-ports 1646 1646",
                "simulator radius host 10.2.2.2 auth-port 1645 acct-port 1646",
            ]
        )
