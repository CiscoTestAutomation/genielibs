import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.system.configure import configure_terminal_settings


class TestConfigureTerminalSettings(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          CS12-19-6:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CS12-19-6']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_terminal_settings(self):
        result = configure_terminal_settings(self.device, 20, 80)
        expected_output = None
        self.assertEqual(result, expected_output)
