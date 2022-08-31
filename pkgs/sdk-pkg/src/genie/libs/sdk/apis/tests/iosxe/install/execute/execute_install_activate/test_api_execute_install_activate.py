import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_activate


class TestExecuteInstallActivate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PI-9300-Stack-103:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PI-9300-Stack-103']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_install_activate(self):
        result = execute_install_activate(self.device, None, True, False, 'True', 'flash:cat9k_iosxe.2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin', 900, 10)
        expected_output = ('$2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin\r\n'
 'install_activate: START Sun Aug 07 12:17:46 UTC 2022\r\n'
 'install_activate: Activating SMU\r\n'
 '--- Starting SMU Activate operation ---\r\n'
 'Performing SMU_ACTIVATE on all members\r\n'
 ' [1] SMU_ACTIVATE package(s) on Switch 1\r\n'
 ' [2] SMU_ACTIVATE package(s) on Switch 2\r\n'
 ' [3] SMU_ACTIVATE package(s) on Switch 3\r\n'
 ' [2] Finished SMU_ACTIVATE on Switch 2\r\n'
 ' [3] Finished SMU_ACTIVATE on Switch 3\r\n'
 ' [1] Finished SMU_ACTIVATE on Switch 1\r\n'
 'Checking status of SMU_ACTIVATE on [1 2 3]\r\n'
 'SMU_ACTIVATE: Passed on [1 2 3]\r\n'
 'Finished SMU Activate operation\r\n'
 '\r\n'
 'SUCCESS: install_activate Sun Aug 07 12:18:00 U')
        self.assertEqual(result, expected_output)
