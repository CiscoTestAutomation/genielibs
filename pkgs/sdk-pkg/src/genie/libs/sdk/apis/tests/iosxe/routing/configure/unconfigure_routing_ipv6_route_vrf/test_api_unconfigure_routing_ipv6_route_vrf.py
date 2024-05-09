import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import unconfigure_routing_ipv6_route_vrf


class TestUnconfigureRoutingIpv6RouteVrf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            model: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['kparames_csr1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_routing_ipv6_route_vrf(self):
        result = unconfigure_routing_ipv6_route_vrf(self.device, '9001::/64', 'OVERLAY', 'GigabitEthernet5', '8001::100')
        expected_output = None
        self.assertEqual(result, expected_output)
