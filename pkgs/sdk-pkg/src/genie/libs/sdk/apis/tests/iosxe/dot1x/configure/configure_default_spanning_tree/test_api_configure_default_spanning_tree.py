import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_default_spanning_tree


class TestConfigureDefaultSpanningTree(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1-9300-SW1:
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
        self.device = self.testbed.devices['T1-9300-SW1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_default_spanning_tree(self):
        result = configure_default_spanning_tree(self.device, 'mode')
        expected_output = None
        self.assertEqual(result, expected_output)
