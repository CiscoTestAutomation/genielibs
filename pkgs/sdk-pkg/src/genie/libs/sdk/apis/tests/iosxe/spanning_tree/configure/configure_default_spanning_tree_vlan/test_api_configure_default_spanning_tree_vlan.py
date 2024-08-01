import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.spanning_tree.configure import configure_default_spanning_tree_vlan


class TestConfigureDefaultSpanningTreeVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          javelin-morph-bgl16-full-tb2-dut1:
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
        self.device = self.testbed.devices['javelin-morph-bgl16-full-tb2-dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_default_spanning_tree_vlan(self):
        result = configure_default_spanning_tree_vlan(self.device, '1-3', 'max-age')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_default_spanning_tree_vlan_1(self):
        result = configure_default_spanning_tree_vlan(self.device, '3-8', None)
        expected_output = None
        self.assertEqual(result, expected_output)
