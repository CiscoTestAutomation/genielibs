from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import unconfigure_service_simulator_radius


class TestUnconfigureServiceSimulatorRadius(TestCase):

    def test_unconfigure_service_simulator_radius(self):
        self.device = Mock()
        unconfigure_service_simulator_radius(
            self.device, client_ip='10.1.1.1',
            access_ports='1812 1812', accounting_ports='1813 1813',
            host_ip='10.2.2.2', auth_port='1812', acct_port='1813'
        )
        self.device.configure.assert_called_once_with(
            [
                "no service simulator radius server",
                "no simulator radius client 10.1.1.1 access-ports"
                " 1812 1812 accounting-ports 1813 1813",
                "no simulator radius host 10.2.2.2"
                " auth-port 1812 acct-port 1813",
            ]
        )
