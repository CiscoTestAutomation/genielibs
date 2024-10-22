import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.flow.execute import execute_monitor_capture_access_list


class TestExecuteMonitorCaptureAccessList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PREG_IFD_CFD_TB3_9500_SA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9500-32QC
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PREG_IFD_CFD_TB3_9500_SA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_monitor_capture_access_list(self):
        result = execute_monitor_capture_access_list(self.device, 'test', 'MYACLV6')
        expected_output = None
        self.assertEqual(result, expected_output)
