import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.spanning_tree.configure import configure_spanning_tree_mst_priority


class TestConfigureSpanningTreeMstPriority(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500L
            type: c9500L
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_spanning_tree_mst_priority(self):
        result = configure_spanning_tree_mst_priority(self.device, 0, 4096)
        expected_output = None
        self.assertEqual(result, expected_output)
