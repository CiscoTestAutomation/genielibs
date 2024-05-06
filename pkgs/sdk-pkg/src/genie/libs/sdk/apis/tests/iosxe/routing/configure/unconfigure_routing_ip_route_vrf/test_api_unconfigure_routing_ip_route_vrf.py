import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import unconfigure_routing_ip_route_vrf


class TestUnconfigureRoutingIpRouteVrf(unittest.TestCase):

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

    def test_unconfigure_routing_ip_route_vrf(self):
        result = unconfigure_routing_ip_route_vrf(self.device, '1.0.0.1', '255.0.0.0', 'UNDERLAY', 'GigabitEthernet10', '11.11.11.2')
        expected_output = None
        self.assertEqual(result, expected_output)
