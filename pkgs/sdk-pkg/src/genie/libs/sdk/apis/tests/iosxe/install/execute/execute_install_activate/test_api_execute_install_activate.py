import unittest
import unittest.mock
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_activate


class TestExecuteInstallActivate(unittest.TestCase):

    def test_execute_install_activate(self):
        self.device = unittest.mock.Mock()
        self.device.execute = unittest.mock.Mock(
            return_value='$2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin\r\n'
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
 'SUCCESS: install_activate Sun Aug 07 12:18:00 U')

        execute_install_activate(self.device, None, True, False, 'True', 'flash:cat9k_iosxe.2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin', 900, 10)
        
        self.assertEqual(self.device.execute.call_count, 1)
        self.assertEqual(
            self.device.execute.call_args[0][0],
            'install activate  file flash:cat9k_iosxe.2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin'
        )
