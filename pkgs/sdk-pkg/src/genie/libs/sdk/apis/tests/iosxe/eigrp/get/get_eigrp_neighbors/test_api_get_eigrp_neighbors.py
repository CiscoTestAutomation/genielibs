import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.get import get_eigrp_neighbors


class TestGetEigrpNeighbors(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R1:
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
        self.device = self.testbed.devices['R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_eigrp_neighbors(self):
        result = get_eigrp_neighbors(self.device, 'default', 3, 'ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_get_eigrp_neighbors_1(self):
        result = get_eigrp_neighbors(self.device, 'default', 3, 'ipv6')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_get_eigrp_neighbors_2(self):
        result = get_eigrp_neighbors(self.device, 'default', 1, 'ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_get_eigrp_neighbors_3(self):
        result = get_eigrp_neighbors(self.device, 'default', 2, 'ipv4')
        expected_output = ['192.168.2.2']
        self.assertEqual(result, expected_output)
