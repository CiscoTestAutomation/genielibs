from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9400.execute import execute_install_one_shot

class TestExecuteInstallOneShot(TestCase):

    def test_execute_install_one_shot(self):
        self.device = Mock()

        results_map = {
            'write memory': """Building configuration...\n[OK]""",
            'install add file flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin activate commit':
                'install_add_activate_commit: START Thu Mar 27 06:52:57 UTC 2025\r\n'
                'install_add: START Thu Mar 27 06:52:57 UTC 2025\r\n'
                'install_add: Adding IMG\r\n'
                ' [1]  R0 Add succeed with reason: Same Image File-No Change  \r\n'
                ' [1]  R1 Add succeed with reason: Same Image File-No Change  \r\n'
                'SUCCESS: install_add_activate_commit '
                '/flash1/user/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin Thu '
                'Mar 27 06:52:57 UTC 2'
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg, "")

        self.device.execute.side_effect = results_side_effect

        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device, 'flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin', 
            True, False, False, 900, 10, False, False, False, False, 30
        )

        expected_output = (
            'install_add_activate_commit: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'install_add: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'install_add: Adding IMG\r\n'
            ' [1]  R0 Add succeed with reason: Same Image File-No Change  \r\n'
            ' [1]  R1 Add succeed with reason: Same Image File-No Change  \r\n'
            'SUCCESS: install_add_activate_commit '
            '/flash1/user/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin Thu '
            'Mar 27 06:52:57 UTC 2'
        )

        self.assertEqual(result.strip(), expected_output.strip())


    def test_execute_install_one_shot_force(self):
        self.device = Mock()

        results_map = {
            'write memory': 'Building configuration...\n[OK]',
            'install add file bootflash://cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250610_001910.SSA.bin activate issu commit force':
                'install_add_activate_commit: START Sun Feb 22 02:43:36 UTC 2015\r\n'
                'install_add_activate_commit: Adding ISSU\r\n'
                'install_add_activate_commit: Checking whether new add is allowed ....\r\n'
                '--- Starting initial file syncing ---\r\n'
                'Copying image file: bootflash:/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250610_001910.SSA.bin to standby\r\n'
                'Info: Finished copying bootflash:/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250610_001910.SSA.bin to standby\r\n'
                'Finished initial file syncing\r\n'
                '--- Starting Add ---\r\n'
                'Performing Add on Active/Standby\r\n'
                '  [1] Add package(s) on R0\r\n'
                '  [1] Add succeed on R0 with reason:"Same Image File-No Change %s"\r\n'
                '  [1] Finished Add on R0\r\n'
                '  [1] Add package(s) on R1\r\n'
                '  [1] Add succeed on R1 with reason:"Same Image File-No Change %s"\r\n'
                '  [1] Finished Add on R1\r\n'
                'Checking status of Add on [R0 R1]\r\n'
                'Add: Passed on [R0 R1]\r\n'
                'Finished Add\r\n'
                'SUCCESS: install_add_activate_commit  Sun Feb 22 02:49:08 UTC 2015\r\n'
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg, "")

        self.device.execute.side_effect = results_side_effect

        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device, 'bootflash://cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250610_001910.SSA.bin', 
            True, True, False, 900, 10, False, False, True, False, 30
        )

        expected_output = (
            'install_add_activate_commit: START Sun Feb 22 02:43:36 UTC 2015\r\n'
            'install_add_activate_commit: Adding ISSU\r\n'
            'install_add_activate_commit: Checking whether new add is allowed ....\r\n'
            '--- Starting initial file syncing ---\r\n'
            'Copying image file: bootflash:/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250610_001910.SSA.bin to standby\r\n'
            'Info: Finished copying bootflash:/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250610_001910.SSA.bin to standby\r\n'
            'Finished initial file syncing\r\n'
            '--- Starting Add ---\r\n'
            'Performing Add on Active/Standby\r\n'
            '  [1] Add package(s) on R0\r\n'
            '  [1] Add succeed on R0 with reason:"Same Image File-No Change %s"\r\n'
            '  [1] Finished Add on R0\r\n'
            '  [1] Add package(s) on R1\r\n'
            '  [1] Add succeed on R1 with reason:"Same Image File-No Change %s"\r\n'
            '  [1] Finished Add on R1\r\n'
            'Checking status of Add on [R0 R1]\r\n'
            'Add: Passed on [R0 R1]\r\n'
            'Finished Add\r\n'
            'SUCCESS: install_add_activate_commit  Sun Feb 22 02:49:08 UTC 2015\r\n'
        )

        self.assertEqual(result.strip(), expected_output.strip())


    def test_execute_install_one_shot_reload(self):
        self.device = Mock()

        results_map = {
            'write memory': """Building configuration...\n[OK]""",
            'install add file flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin activate commit':
                'install_add_activate_commit: START Thu Mar 27 06:52:57 UTC 2025\r\n'
                'install_add: START Thu Mar 27 06:52:57 UTC 2025\r\n'
                'install_add: Adding IMG\r\n'
                ' [1]  R0 Add succeed with reason: Same Image File-No Change  \r\n'
                ' [1]  R1 Add succeed with reason: Same Image File-No Change  \r\n'
                'SUCCESS: install_add_activate_commit '
                '/flash1/user/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin Thu '
                'Mar 27 06:52:57 UTC 2'
                'Initializing Hardware ...\r\n'
                'System Bootstrap, Version 17.6.1r[FC2], RELEASE SOFTWARE (P) \r\n'
                'Compiled Wed 05/12/2021 15:39:34.01 by rel \r\n'
                'Current ROMMON image : Primary \r\n'
                'Last reset cause     : SoftwareResetTrig \r\n'
                'C9400-SUP-1 platform with 16777216 Kbytes of main memory \r\n'
                'Cisco IOS Software [IOSXE], Catalyst L3 Switch Software (CAT9K_IOSXE), Experimental Version 17.15.20250916:185810 [BLD_V1715_THROTTLE_LATEST_20250916_173856:/nobackup/mcpre/s2c-build-ws 101] '
                'Copyright (c) 1986-2025 by Cisco Systems, Inc. '
                'Compiled Tue 16-Sep-25 18:58 by mcpre '
                'Press RETURN to get started!'
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg, "")

        self.device.execute.side_effect = results_side_effect

        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device, 'flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin', 
            True, False, False, 900, 10, False, False, False, True, 30
        )

        expected_output = (
            'install_add_activate_commit: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'install_add: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'install_add: Adding IMG\r\n'
            ' [1]  R0 Add succeed with reason: Same Image File-No Change  \r\n'
            ' [1]  R1 Add succeed with reason: Same Image File-No Change  \r\n'
            'SUCCESS: install_add_activate_commit '
            '/flash1/user/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin Thu '
            'Mar 27 06:52:57 UTC 2'
            'Initializing Hardware ...\r\n'
            'System Bootstrap, Version 17.6.1r[FC2], RELEASE SOFTWARE (P) \r\n'
            'Compiled Wed 05/12/2021 15:39:34.01 by rel \r\n'
            'Current ROMMON image : Primary \r\n'
            'Last reset cause     : SoftwareResetTrig \r\n'
            'C9400-SUP-1 platform with 16777216 Kbytes of main memory \r\n'
            'Cisco IOS Software [IOSXE], Catalyst L3 Switch Software (CAT9K_IOSXE), Experimental Version 17.15.20250916:185810 [BLD_V1715_THROTTLE_LATEST_20250916_173856:/nobackup/mcpre/s2c-build-ws 101] '
            'Copyright (c) 1986-2025 by Cisco Systems, Inc. '
            'Compiled Tue 16-Sep-25 18:58 by mcpre '
            'Press RETURN to get started!'
        )

        self.assertEqual(result.strip(), expected_output.strip())

