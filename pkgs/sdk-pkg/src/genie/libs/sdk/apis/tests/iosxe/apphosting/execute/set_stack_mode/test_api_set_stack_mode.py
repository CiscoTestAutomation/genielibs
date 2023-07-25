import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.execute import set_stack_mode


class TestSetStackMode(unittest.TestCase):

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

    def test_set_stack_mode(self):
        result = set_stack_mode('T1-9300-SW1', 10, 12)
        expected_output = None
        self.assertEqual(result, expected_output)
