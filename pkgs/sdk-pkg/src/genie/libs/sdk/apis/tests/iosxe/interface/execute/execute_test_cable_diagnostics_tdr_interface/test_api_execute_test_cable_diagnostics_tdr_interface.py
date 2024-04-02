import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.execute import execute_test_cable_diagnostics_tdr_interface


class TestExecuteTestCableDiagnosticsTdrInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IE-3300-8P2S-E3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ie3300
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IE-3300-8P2S-E3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_test_cable_diagnostics_tdr_interface(self):
        result = execute_test_cable_diagnostics_tdr_interface(self.device, 'GigabitEthernet1/4')
        expected_output = ('TDR test started on interface Gi1/4\r\n'
 'A TDR test can take a few seconds to run on an interface\r\n'
 "Use 'show cable-diagnostics tdr' to read the TDR results.")
        self.assertEqual(result, expected_output)
