import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_diagnostic_monitor_threshold


class TestUnconfigDiagnosticMonitorThreshold(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Nyquist-9300-Stack:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Nyquist-9300-Stack']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_diagnostic_monitor_threshold(self):
        result = unconfig_diagnostic_monitor_threshold(self.device, 2, 6, 4)
        expected_output = None
        self.assertEqual(result, expected_output)
