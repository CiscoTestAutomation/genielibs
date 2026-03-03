from unittest import TestCase
from unittest.mock import Mock, call, patch
from genie.libs.sdk.apis.iosxe.cat9k.c9400.execute import execute_install_one_shot


class TestExecuteInstallOneShot(TestCase):

    def test_execute_install_one_shot(self):
        """Test basic install one shot via execute path (install_reload=False)"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        install_output = (
            'install_add_activate_commit: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'install_add: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'install_add: Adding IMG\r\n'
            ' [1]  R0 Add succeed with reason: Same Image File-No Change  \r\n'
            ' [1]  R1 Add succeed with reason: Same Image File-No Change  \r\n'
            'SUCCESS: install_add_activate_commit '
            '/flash1/user/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin Thu '
            'Mar 27 06:52:57 UTC 2'
        )

        results_map = {
            'write memory': 'Building configuration...\n[OK]',
            'install add file flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin activate commit':
                install_output
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg, "")

        self.device.execute.side_effect = results_side_effect
        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device,
            file_path='flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin',
            prompt=True,
            issu=False,
            negative_test=False,
            timeout=900,
            connect_timeout=10,
            install_reload=False,
        )

        self.device.api.execute_write_memory.assert_called_once()
        self.device.execute.assert_called_once()
        self.assertEqual(result.strip(), install_output.strip())

    def test_execute_install_one_shot_force(self):
        """Test install one shot with issu=True and force=True via execute path"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        install_output = (
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

        results_map = {
            'write memory': 'Building configuration...\n[OK]',
            'install add file bootflash://cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250610_001910.SSA.bin activate issu commit force':
                install_output
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg, "")

        self.device.execute.side_effect = results_side_effect
        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device,
            file_path='bootflash://cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250610_001910.SSA.bin',
            prompt=True,
            issu=True,
            negative_test=False,
            timeout=900,
            connect_timeout=10,
            force=True,
            install_reload=False,
        )

        self.device.api.execute_write_memory.assert_called_once()
        self.device.execute.assert_called_once()
        self.assertEqual(result.strip(), install_output.strip())

    def test_execute_install_one_shot_reload(self):
        """Test install one shot via reload path (install_reload=True)"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        reload_output = (
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
            'Press RETURN to get started!'
        )

        # device.reload returns (success_flag, output) when return_output=True
        self.device.reload = Mock(return_value=(True, reload_output))
        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device,
            file_path='flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin',
            prompt=True,
            issu=False,
            negative_test=False,
            timeout=900,
            connect_timeout=10,
            install_reload=True,
        )

        self.device.api.execute_write_memory.assert_called_once()
        self.device.reload.assert_called_once()
        # Verify key reload kwargs
        reload_call_kwargs = self.device.reload.call_args[1]
        self.assertTrue(reload_call_kwargs['return_output'])
        self.assertTrue(reload_call_kwargs['prompt_recovery'])
        self.assertEqual(reload_call_kwargs['error_pattern'], [])
        self.assertEqual(result.strip(), reload_output.strip())

    def test_execute_install_one_shot_reload_with_error_pattern(self):
        """Test install one shot reload path passes error_pattern through"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        reload_output = 'SUCCESS: install_add_activate_commit\r\n'
        self.device.reload = Mock(return_value=(True, reload_output))
        self.device.api.execute_write_memory = Mock()

        custom_errors = ['FAILED', 'ERROR']
        result = execute_install_one_shot(
            self.device,
            file_path='flash:test.bin',
            install_reload=True,
            error_pattern=custom_errors,
        )

        reload_call_kwargs = self.device.reload.call_args[1]
        self.assertEqual(reload_call_kwargs['error_pattern'], custom_errors)
        self.assertNotEqual(result, False)

    def test_execute_install_one_shot_failed(self):
        """Test install one shot returns False when output contains FAILED"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        failed_output = (
            'install_add_activate_commit: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'FAILED: install_add_activate_commit\r\n'
        )

        self.device.execute = Mock(return_value=failed_output)
        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device,
            file_path='flash:bad_image.bin',
            install_reload=False,
        )

        self.assertFalse(result)

    def test_execute_install_one_shot_negative_test(self):
        """Test negative_test=True returns False when output contains SUCCESS"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        success_output = 'SUCCESS: install_add_activate_commit\r\n'
        self.device.execute = Mock(return_value=success_output)
        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device,
            file_path='flash:test.bin',
            negative_test=True,
            install_reload=False,
        )

        # For negative_test, SUCCESS in output means fail
        self.assertFalse(result)

    def test_execute_install_one_shot_xfsu(self):
        """Test install one shot with xfsu flag in command"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        install_output = 'SUCCESS: install_add_activate_commit\r\n'
        self.device.execute = Mock(return_value=install_output)
        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device,
            file_path='flash:test.bin',
            xfsu=True,
            install_reload=False,
        )

        cmd = self.device.execute.call_args[0][0]
        self.assertIn('xfsu', cmd)
        self.assertNotEqual(result, False)

    def test_execute_install_one_shot_reloadfast(self):
        """Test install one shot with reloadfast flag in command"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        install_output = 'SUCCESS: install_add_activate_commit\r\n'
        self.device.execute = Mock(return_value=install_output)
        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device,
            file_path='flash:test.bin',
            reloadfast=True,
            install_reload=False,
        )

        cmd = self.device.execute.call_args[0][0]
        self.assertIn('reloadfast', cmd)
        self.assertNotEqual(result, False)

    def test_execute_install_one_shot_prompt_level_none(self):
        """Test install one shot with prompt=False adds 'prompt-level none'"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.subconnections = None

        install_output = 'SUCCESS: install_add_activate_commit\r\n'
        self.device.execute = Mock(return_value=install_output)
        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device,
            file_path='flash:test.bin',
            prompt=False,
            install_reload=False,
        )

        cmd = self.device.execute.call_args[0][0]
        self.assertIn('prompt-level none', cmd)
