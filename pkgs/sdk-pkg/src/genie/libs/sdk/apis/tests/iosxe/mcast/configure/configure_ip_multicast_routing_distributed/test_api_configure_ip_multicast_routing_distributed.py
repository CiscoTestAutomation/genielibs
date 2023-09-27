import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mcast.configure import configure_ip_multicast_routing_distributed


class TestConfigureIpMulticastRoutingDistributed(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          KS1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C8300-1N1S-4T2X
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['KS1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_multicast_routing_distributed(self):
        result = configure_ip_multicast_routing_distributed(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
