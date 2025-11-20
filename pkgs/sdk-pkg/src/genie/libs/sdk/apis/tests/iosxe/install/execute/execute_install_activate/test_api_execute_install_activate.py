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

class TestExecuteInstallActivateReload(unittest.TestCase):

    def test_execute_install_activate_with_reload_support(self):
        """
        Tests the execute_install_activate function with install_reload=True,
        simulating a successful install activate followed by a device reload.
        """
        self.device = unittest.mock.Mock()
        install_activate_output_part = (
            '$2025-09-18T13:30:01: %UNICON-6-INFO: +++ ott-c9400-01(alias=uut) with via \'b\' and alias \'b\': executing command \'install activate \' +++ \r\n'
            'install activate  \r\n'
            'install_activate: START Wed Jan 07 17:53:29 UTC 2015 \r\n'
            'install_activate: Activating IMG \r\n'
            'Following packages shall be activated: \r\n'
            '/bootflash/cat9k-cc_srdriver.BLD_V1718_THROTTLE_LATEST_20250915_224459.SSA.pkg \r\n'
            '... (other package lines) ... \r\n'
            'This operation may require a reload of the system. Do you want to proceed? [y/n]y \r\n'
            '— Starting Activate — \r\n'
            'Performing Activate on all members \r\n'
            '[1] Activate package(s) on  R1 \r\n'
            '[1] Activate package(s) on  R0 \r\n'
            '[1] Finished Activate on  R0 \r\n'
            '[1] Finished Activate on  R1 \r\n'
            'Checking status of Activate on [R0 R1] \r\n'
            'Activate: Passed on [R0 R1] \r\n'
            'Finished Activate \r\n'
            'SUCCESS: install_activate Wed Jan 07 17:55:04 UTC 2015 \r\n'
        )
        reload_boot_output_part = (
            'Initializing Hardware ...\r\n'
            'System Bootstrap, Version 17.6.1r[FC2], RELEASE SOFTWARE (P) \r\n'
            'Compiled Wed 05/12/2021 15:39:34.01 by rel \r\n'
            'Current ROMMON image : Primary \r\n'
            'Last reset cause     : SoftwareResetTrig \r\n'
            'C9400-SUP-1 platform with 16777216 Kbytes of main memory \r\n'
            'Cisco IOS Software [IOSXE], Catalyst L3 Switch Software (CAT9K_IOSXE), Experimental Version 17.15.20250916:185810 [BLD_V1715_THROTTLE_LATEST_20250916_173856:/nobackup/mcpre/s2c-build-ws 101] \r\n'
            'Copyright (c) 1986-2025 by Cisco Systems, Inc. \r\n'
            'Compiled Tue 16-Sep-25 18:58 by mcpre \r\n'
            'Press RETURN to get started!'
        )
        full_mock_reload_output = install_activate_output_part + reload_boot_output_part
        self.device.reload = unittest.mock.Mock(return_value=(True, full_mock_reload_output))
        expected_command = 'install activate  issu auto-abort-timer 300'
        result = execute_install_activate(
            self.device,
            abort_timer='300',
            prompt=True,
            issu=True,
            smu=False,
            file_name=None,
            timeout=1200,
            connect_timeout=10,
            post_reload_wait_time=300,
            error_pattern=['Error', 'Failed to install'],
            install_reload=True
        )
        self.device.api.execute_write_memory.assert_called_once()
        self.device.reload.assert_called_once_with(
            expected_command,
            reply=unittest.mock.ANY,
            timeout=1200,
            return_output=True,
            prompt_recovery=True,
            post_reload_wait_time=300,
            error_pattern=['Error', 'Failed to install']
        )
        self.assertEqual(result, full_mock_reload_output)
        self.assertIn("SUCCESS: install_activate", result)