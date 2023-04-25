import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import remove_routing_ip_route


class TestRemoveRoutingIpRoute(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          n08HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['n08HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_remove_routing_ip_route(self):
        result = remove_routing_ip_route(self.device, '1.1.1.1', '255.255.255.255', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
