import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import unconfig_ip_on_vlan


class TestUnconfigIpOnVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          AMZ-Acc-4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['AMZ-Acc-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_ip_on_vlan(self):
        result = unconfig_ip_on_vlan(self.device, '101', '10.230.62.50', '255.255.255.0', None, None, True)
        expected_output = None
        self.assertEqual(result, expected_output)
