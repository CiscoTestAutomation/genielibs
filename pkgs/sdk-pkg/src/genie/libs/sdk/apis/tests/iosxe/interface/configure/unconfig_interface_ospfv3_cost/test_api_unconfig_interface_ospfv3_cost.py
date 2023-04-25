import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_interface_ospfv3_cost


class TestUnconfigInterfaceOspfv3Cost(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ASR1013:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ASR1013']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_interface_ospfv3_cost(self):
        result = unconfig_interface_ospfv3_cost(self.device, 'GigabitEthernet0/1/0', '1', '100', None, None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfig_interface_ospfv3_cost_1(self):
        result = unconfig_interface_ospfv3_cost(self.device, 'GigabitEthernet0/1/0', '1', None, '10', None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfig_interface_ospfv3_cost_2(self):
        result = unconfig_interface_ospfv3_cost(self.device, 'GigabitEthernet0/1/0', '1', None, None, '50', None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfig_interface_ospfv3_cost_3(self):
        result = unconfig_interface_ospfv3_cost(self.device, 'GigabitEthernet0/1/0', '1', None, None, None, '40', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfig_interface_ospfv3_cost_4(self):
        result = unconfig_interface_ospfv3_cost(self.device, 'GigabitEthernet0/1/0', '1', None, None, None, None, '30', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfig_interface_ospfv3_cost_5(self):
        result = unconfig_interface_ospfv3_cost(self.device, 'GigabitEthernet0/1/0', '1', None, None, None, None, None, '20')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfig_interface_ospfv3_cost_6(self):
        result = unconfig_interface_ospfv3_cost(self.device, 'GigabitEthernet0/1/0', '1', None, None, None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
