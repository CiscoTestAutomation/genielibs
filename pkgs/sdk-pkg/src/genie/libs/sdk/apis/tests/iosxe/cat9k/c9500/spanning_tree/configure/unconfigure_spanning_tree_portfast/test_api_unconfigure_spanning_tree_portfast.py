import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9500.spanning_tree.configure import unconfigure_spanning_tree_portfast


class TestUnconfigureSpanningTreePortfast(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_spanning_tree_portfast(self):
        result = unconfigure_spanning_tree_portfast(self.device, True, True, False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_spanning_tree_portfast_1(self):
        result = unconfigure_spanning_tree_portfast(self.device, False, True, False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_spanning_tree_portfast_2(self):
        result = unconfigure_spanning_tree_portfast(self.device, True, False, True)
        expected_output = None
        self.assertEqual(result, expected_output)
