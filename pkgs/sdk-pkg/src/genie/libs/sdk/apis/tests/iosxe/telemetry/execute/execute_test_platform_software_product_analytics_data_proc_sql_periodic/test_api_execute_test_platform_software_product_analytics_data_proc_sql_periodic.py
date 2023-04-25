import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.telemetry.execute import execute_test_platform_software_product_analytics_data_proc_sql_periodic


class TestExecuteTestPlatformSoftwareProductAnalyticsDataProcSqlPeriodic(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch_48U:
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
        self.device = self.testbed.devices['Switch_48U']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_test_platform_software_product_analytics_data_proc_sql_periodic(self):
        result = execute_test_platform_software_product_analytics_data_proc_sql_periodic(self.device)
        expected_output = ''
        self.assertEqual(result, expected_output)
