import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.spanning_tree.verify import verify_spanning_tree_root_inc


class TestVerifySpanningTreeRootInc(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          E-9300-STACK:
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
        self.device = self.testbed.devices['E-9300-STACK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_spanning_tree_root_inc(self):
        result = verify_spanning_tree_root_inc(self.device, '300', 'TenGigabitEthernet4/1/3')
        expected_output = True
        self.assertEqual(result, expected_output)
