import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.execute import execute_clear_console


class TestExecuteClearConsole(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Fnc-c9300:
            connections:
              defaults:
                class: unicon.Unicon
              telnet:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Fnc-c9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[],
            via='telnet',
        )

    def test_execute_clear_console(self):
        result = execute_clear_console(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
