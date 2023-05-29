import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import config_interface_ospfv3_network_type


class TestConfigInterfaceOspfv3NetworkType(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Router:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ASR1K
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_interface_ospfv3_network_type_ipv6(self):
        result = config_interface_ospfv3_network_type(self.device, 'vmi1', '1', 'point-to-point', 'ipv6')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_config_interface_ospfv3_network_type_ipv4(self):
        result = config_interface_ospfv3_network_type(self.device, 'vmi1', '1', 'point-to-point', 'ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_config_interface_ospfv3_network_type_both(self):
        result = config_interface_ospfv3_network_type(self.device, 'vmi1', '1', 'point-to-point', 'both')
        expected_output = None
        self.assertEqual(result, expected_output)
