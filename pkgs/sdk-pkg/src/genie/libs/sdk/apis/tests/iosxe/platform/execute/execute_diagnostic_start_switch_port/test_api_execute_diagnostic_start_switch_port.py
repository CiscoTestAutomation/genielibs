import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_diagnostic_start_switch_port


class TestExecuteDiagnosticStartSwitchPort(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SA-C9350-24P:
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
        self.device = self.testbed.devices['SA-C9350-24P']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_diagnostic_start_switch_port(self):
        result = execute_diagnostic_start_switch_port(self.device, 1, '4', '2')
        expected_output = None
        self.assertEqual(result, expected_output)
