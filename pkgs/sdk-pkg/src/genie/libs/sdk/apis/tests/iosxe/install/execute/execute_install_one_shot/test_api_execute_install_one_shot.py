import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_one_shot


class TestExecuteInstallOneShot(unittest.TestCase):

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

    def test_execute_install_one_shot(self):
        result = execute_install_one_shot(self.device, 'bootflash:cat9k_iosxe.2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin', True, False, 900, 10)
        expected_output = ('$2.21_mcpre.24042.CSCvq24042.SSA.smu.bin activate commit\r\n'
 'install_add_activate_commit: START Sun Aug 07 12:36:41 UTC 2022\r\n'
 'install_add: START Sun Aug 07 12:36:41 UTC 2022\r\n'
 'install_add: Adding IMG\r\n'
 '--- Starting initial file syncing ---\r\n'
 'Copying '
 'flash:cat9k_iosxe.2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin from '
 'Switch 1 to Switch 1 2 3\r\n'
 'Info: Finished copying to the selected Switch\r\n'
 'Finished initial file syncing\r\n'
 '\r\n'
 '--- Starting SMU Add operation ---\r\n'
 'Performing SMU_ADD on all members\r\n'
 'Checking status of SMU_ADD on [1 2 3]\r\n'
 'SMU_ADD: Passed on [1 2 3]\r\n'
 'Finished SMU Add operation\r\n'
 '\r\n'
 'install_activate: START Sun Aug 07 12:36:47 UTC 2022\r\n'
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
 '--- Starting Commit ---\r\n'
 'Performing Commit on all members\r\n'
 '--- Starting SMU Commit ---\r\n'
 ' [1] Commit package(s) on Switch 1\r\n'
 ' [2] Commit package(s) on Switch 2\r\n'
 ' [3] Commit package(s) on Switch 3\r\n'
 ' [2] Finished Commit on Switch 2\r\n'
 ' [1] Finished Commit on Switch 1\r\n'
 ' [3] Finished Commit on Switch 3\r\n'
 'Checking status of Commit on [1 2 3]\r\n'
 'Commit: Passed on [1 2 3]\r\n'
 'Finished Commit operation\r\n'
 '\r\n'
 'SUCCESS: install_add_activate_commit Sun Aug 07 12:37:05 UTC 2022')
        self.assertEqual(result, expected_output)
