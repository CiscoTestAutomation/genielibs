import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.telemetry.verify import verify_telemetry_report_in_show_summary


class TestVerifyTelemetryReportInShowSummary(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_telemetry_report_in_show_summary(self):
        result = verify_telemetry_report_in_show_summary(self.device, 1668458555)
        expected_output = True
        self.assertEqual(result, expected_output)
