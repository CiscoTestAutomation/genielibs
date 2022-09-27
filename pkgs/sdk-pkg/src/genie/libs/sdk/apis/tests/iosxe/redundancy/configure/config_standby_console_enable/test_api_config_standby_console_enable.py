import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.redundancy.configure import config_standby_console_enable


class TestConfigStandbyConsoleEnable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          C9410-gen2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C9410-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_standby_console_enable(self):
        result = config_standby_console_enable(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
