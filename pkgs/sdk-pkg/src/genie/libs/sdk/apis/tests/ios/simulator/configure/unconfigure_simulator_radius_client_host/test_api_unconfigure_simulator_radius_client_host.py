from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import (
    unconfigure_simulator_radius_client_host,
)


class TestUnconfigureSimulatorRadiusClientHost(TestCase):

    def test_unconfigure_simulator_radius_client_host(self):
        self.device = Mock()
        unconfigure_simulator_radius_client_host(
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
                "no simulator radius client 10.1.1.1 access-ports 1645 1645"
                " accounting-ports 1646 1646",
                "no simulator radius host 10.2.2.2 auth-port 1645"
                " acct-port 1646",
            ]
        )
