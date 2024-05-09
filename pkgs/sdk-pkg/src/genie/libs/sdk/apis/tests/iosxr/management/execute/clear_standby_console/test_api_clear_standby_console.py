import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxr.management.execute import clear_standby_console


class TestClearStandbyConsole(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxr --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxr
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_standby_console(self):
        result = clear_standby_console(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
