import logging
import unittest
import re
from unittest.mock import Mock, MagicMock, call, ANY, patch, PropertyMock
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.stages import InstallImage
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device
from genie.libs.sdk.apis.iosxe.platform.verify import verify_boot_variable as sdk_verify_boot_variable

from pyats.easypy import runtime
from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped, Passx
from pyats.aetest.signals import TerminateStepSignal, AEtestSkippedSignal, AEtestStepPassxSignal


import unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import TimeoutError as UniconTimeoutError

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class DeleteBootVariable(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_boot_variable(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_delete_boot_variables(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure method to raise an exception when called.
        # This simulates the fail case.
        self.device.configure = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.delete_boot_variable(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class SetBootVariable(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        data = {'dir bootflash:/': '''
                   Directory of bootflash:/
                        11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                        12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                        104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                        80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                        64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                        48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                        8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  test.bin
                        1940303872 bytes total (1036210176 bytes free)
                '''
                }

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(return_value = data['dir bootflash:/'])

        self.device.api.create_empty_file = Mock()

        # And we want the execute_set_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.api.execute_set_boot_variable = Mock()
        self.device.api.unconfigure_ignore_startup_config = Mock()
        # Call the method to be tested (clean step inside class)
        self.cls.set_boot_variable(
            steps=steps, device=self.device
        )
        self.device.api.create_empty_file.assert_called_once_with(
            'bootflash:/', 'packages.conf', overwrite=False)
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_set_boot_variables(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = {'dir bootflash:/': '''
                   Directory of bootflash:/
                        11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                        12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                        104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                        80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                        64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                        48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                        8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  test.bin
                        1940303872 bytes total (1036210176 bytes free)
                '''
                }

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(return_value = data['dir bootflash:/'])

        self.device.api.create_empty_file = Mock()

        # And we want the execute_set_boot_variable api to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_set_boot_variable = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.set_boot_variable(
                steps=steps, device=self.device
            )

        self.device.api.create_empty_file.assert_called_once_with(
            'bootflash:/', 'packages.conf', overwrite=False)
        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
        

    def test_passx_set_boot_variables_unconfigure_ignore_startup_config_errored(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = {'dir bootflash:/': '''
                   Directory of bootflash:/
                        11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                        12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                        104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                        80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                        64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                        48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                        8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  test.bin
                        1940303872 bytes total (1036210176 bytes free)
                '''
                }

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(return_value = data['dir bootflash:/'])

        self.device.api.create_empty_file = Mock()

        # And we want the execute_set_boot_variable
        self.device.api.execute_set_boot_variable = Mock()
        
        self.cls.set_boot_variable(
                steps=steps, device=self.device
            )

        self.device.api.create_empty_file.assert_called_once_with(
            'bootflash:/', 'packages.conf', overwrite=False)
        # Check the overall result is as expected
        self.assertEqual(Passed, steps.details[0].result)

class SaveRunningConfig(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_copy_run_to_start api to be mocked.
        # This simulates the pass case.
        self.device.api.execute_copy_run_to_start = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.save_running_config(
            steps=steps, device=self.device
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_save_running_config(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_copy_run_to_start api to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_copy_run_to_start = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.save_running_config(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
    
    def test_skipped(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_copy_run_to_start api to be mocked.
        # This simulates the pass case.
        self.device.api.execute_copy_run_to_start = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.save_running_config(
            steps=steps, device=self.device, skip_save_running_config=True
        )
        # Check that the result is expected
        self.assertEqual(Skipped, steps.details[0].result)


class VerifyBootVariable(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='cat9k')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.cls.new_boot_var = 'bootflash:cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin'

        data1 = {'show boot': '''
            starfleet-1#show boot
            BOOT variable = bootflash:cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin;
            Configuration Register is 0x102
            MANUAL_BOOT variable = no
            BAUD variable = 9600
            ENABLE_BREAK variable does not exist
            BOOTMODE variable does not exist
            IPXE_TIMEOUT variable does not exist
            CONFIG_FILE variable =
        '''
        }

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock(return_value=data1['show boot'])
        self.device.api.verify_boot_variable = Mock(return_value=True)
        self.device.api.verify_ignore_startup_config = Mock(return_value=False)

        # Call the method to be tested (clean step inside class)
        self.cls.verify_boot_variable(
            steps=steps, device=self.device
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_verify_boot_variables(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.cls.new_boot_var = 'flash:cat9k_iosxe.BLD_V173_999.SSA.bin'

        data1 = {'show boot': '''
            starfleet-1#show boot
            BOOT variable = bootflash:cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin;
            Configuration Register is 0x102
            MANUAL_BOOT variable = no
            BAUD variable = 9600
            ENABLE_BREAK variable does not exist
            BOOTMODE variable does not exist
            IPXE_TIMEOUT variable does not exist
            CONFIG_FILE variable =
        '''
        }

        # Simulate API mismatch: expected new_boot_var is not in next boot vars.
        self.device.execute = Mock(return_value=data1['show boot'])
        self.device.api.get_boot_variables = Mock(
            return_value=['bootflash:cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin']
        )
        self.device.api.verify_boot_variable = Mock(
            side_effect=lambda boot_images: sdk_verify_boot_variable(
                device=self.device,
                boot_images=boot_images
            )
        )

        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_boot_variable(
                steps=steps, device=self.device
            )

        self.device.api.get_boot_variables.assert_called_once_with(boot_var='next', output=None)
        self.device.api.verify_boot_variable.assert_called_once_with(
            boot_images=[self.cls.new_boot_var]
        )
        self.assertEqual(Failed, steps.details[0].result)

class Installimage(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')
        self.device.spawn = Mock()

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_pass(self, dialog):
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        images = ['/auto/some-location/that-this/image/stay-isr-image.bin']
        self.cls.new_boot_var = 'flash:cat9k_iosxe.BLD_V173_999.SSA.bin'
        self.cls.history = OrderedDict()
        self.cls.mock_value = OrderedDict()
        setattr(self.cls.mock_value, 'parameters', {})
        self.cls.history.update({'InstallImage': self.cls.mock_value})
        self.cls.history['InstallImage'].parameters =  OrderedDict()

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.reload = Mock()
        # self.device.execute = Mock()
        self.device.parse = Mock(return_value={
                                 'location': {
                                     'Switch 1': {
                                         'pkg_state': {
                                             1: {'type': 'IMG',
                                                 'state': 'U',
                                                 'filename_version': '17.17.01.0.207986'}},
                                         'auto_abort_timer': 'inactive'
                                         }}})

        output = '''
        install_commit: START Thu Jun 05 01:16:12 UTC 2025
        --- Starting Commit ---
        Performing Commit on all members
        [1] Commit packages(s) on Switch 1
        [1] Finished Commit packages(s) on Switch 1
        Checking status of Commit on [1]
        Commit: Passed on [1]
        Finished Commit operation
        SUCCESS: install_commit
        '''
        self.device.execute = Mock(return_value = output)

        self.device.api.get_running_image = Mock()
        # Call the method to be tested (clean step inside class)
        self.cls.install_image(
            steps=steps, device=self.device, images=images
        )
        # Check that the result is expected

        self.assertEqual('Check for previous uncommitted install operation', steps.details[0].name)
        self.assertEqual("Installing image '/auto/some-location/that-this/image/stay-isr-image.bin'", steps.details[1].name)
        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Passed, steps.details[1].result)

    def test_fail_to_install_image(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        images = ['/auto/some-location/that-this/image/stay-isr-image.bin']
        self.cls.history = {}

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the fail case.
        self.device.reload = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.install_image(
                steps=steps, device=self.device, images=images
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class TestInstallImage(unittest.TestCase):

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_iosxe_install_image_pass(self, dialog):
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.reload = Mock()
        device.parse = Mock(return_value={
                                 'location': {
                                     'Switch 1': {
                                         'pkg_state': {
                                             1: {'type': 'IMG',
                                                 'state': 'C',
                                                 'filename_version': '17.17.01.0.207986'}},
                                         'auto_abort_timer': 'inactive'
                                         }}})

        device.api.get_running_image = Mock()
        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])

        expected_execute_call = [call('install add file sftp://server/image.bin activate commit prompt-level none',
                                 reply=reload_dialog,
                                 append_error_pattern=['FAILED:'],
                                 timeout=500),
                                 call('install commit')]

        device.execute.assert_has_calls(expected_execute_call)
        expected_reload_call = call(
                '',
                reload_creds='default',
                prompt_recovery=True,
                error_pattern=['FAILED:.*?$'],
                device_recovery=False,
                timeout=500,
                reply=reload_dialog,
            )
        device.reload.assert_has_calls([expected_reload_call])
        self.assertEqual(Passed, steps.details[0].result)

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_iosxe_install_image_success_before_reload_timeout(self, dialog):
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.spawn = Mock()
        device.reload = Mock()
        device.parse = Mock(return_value={
                                 'location': {
                                     'Switch 1': {
                                         'pkg_state': {
                                             1: {'type': 'IMG',
                                                 'state': 'C',
                                                 'filename_version': '17.17.01.0.207986'}},
                                         'auto_abort_timer': 'inactive'
                                         }}})

        device.api.get_running_image = Mock(return_value='old_image.bin')
        device.api.collect_install_log = Mock()
        device.execute = Mock(side_effect=[
            Exception("SUCCESS: install_add_activate_commit\nreboot: Restarting system"),
            "SUCCESS:",
        ])

        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])

        device.api.collect_install_log.assert_not_called()
        expected_execute_call = [
            call('install add file sftp://server/image.bin activate commit prompt-level none',
                 reply=reload_dialog,
                 append_error_pattern=['FAILED:'],
                 timeout=500),
            call('install commit')
        ]
        device.execute.assert_has_calls(expected_execute_call)
        device.reload.assert_called_once_with(
            '',
            reload_creds='default',
            prompt_recovery=True,
            error_pattern=['FAILED:.*?$'],
            device_recovery=False,
            timeout=500,
            reply=reload_dialog,
        )
        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Passed, steps.details[1].result)

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_iosxe_install_image_reload_dialog_matches_c9350_quick_reload(self, dialog):
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.spawn = Mock()
        device.reload = Mock()
        device.parse = Mock(return_value={
                                 'location': {
                                     'Switch 1': {
                                         'pkg_state': {
                                             1: {'type': 'IMG',
                                                 'state': 'C',
                                                 'filename_version': '17.17.01.0.207986'}},
                                         'auto_abort_timer': 'inactive'
                                         }}})

        device.api.get_running_image = Mock(return_value='old_image.bin')
        device.execute = Mock(side_effect=[
            "SUCCESS: install_add_activate_commit",
            "SUCCESS:",
        ])

        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])

        check_reload_statements = dialog.call_args_list[1][0][0]
        check_reload_patterns = [statement.pattern for statement in check_reload_statements]
        c9350_quick_reload_outputs = [
            "R0/0: pvp: Process manager is exiting: reload fru action requested",
            "Chassis 1 reloading, reason - Reload Command",
            "Chassis 1 reloading firmware, reason - Reload Firmware Command",
        ]

        for output in c9350_quick_reload_outputs:
            self.assertTrue(
                any(re.match(pattern, output) for pattern in check_reload_patterns),
                f"No reload dialog pattern matched {output!r}")

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_iosxe_install_image_pass_retries_not_enough_space(self, dialog):
        reload_dialog = Mock()
        dialog_statements = []

        def _dialog(statements):
            dialog_statements.append(statements)
            return reload_dialog

        dialog.side_effect = _dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'
        
        package_data = '''boot   rp 0 0   rp_boot cat9k.pkg
boot   rp 1 0   rp_boot cat9k-1.pkg
iso   rp 0 0   rp_base cat9k-2.pkg'''
        
        device = create_test_device('PE1', os='iosxe')
        device.reload = Mock()
        device.spawn = Mock()
        device.is_ha = False
        execute_responses = iter([
            'Directory of bootflash:/', package_data, "bootflash", "", ""
        ])

        def _execute(cmd, **kwargs):
            if (cmd == 'install add file bootflash:/image.bin activate '
                    'commit prompt-level none' and not hasattr(device, 'space_required')):
                output = (
                    'FAILED: flash: requires 455144 KB of free space, '
                    'but only 99460 KB is available\n'
                    'FAILED: install_add  exit(1)'
                )
                space_statement = next(
                    statement for statement in dialog_statements[0]
                    if re.search(statement.pattern, output)
                    and getattr(statement, 'action', None)
                    and statement.action.__name__ == '_check_disk_space'
                )
                spawn = Mock(buffer=output, device=device)
                space_statement.action(spawn, None, None)
                raise Exception(output)
            return next(execute_responses)

        device.execute = Mock(side_effect=_execute)
        device.parse = Mock(return_value={
                                 'location': {
                                     'Switch 1': {
                                         'pkg_state': {
                                             1: {'type': 'IMG',
                                                 'state': 'C',
                                                 'filename_version': '17.17.01.0.207986'}},
                                         'auto_abort_timer': 'inactive'
                                         }}})

        device.api.get_running_image = Mock()
        device.api.collect_install_log = Mock()
        device.api.free_up_disk_space = Mock(return_value=True)
        cls.install_image(steps=steps, device=device, images=['bootflash:/image.bin'])

        install_failure_statement = next(
            statement for statement in dialog_statements[0]
            if 'FAILED: install_add' in str(statement.pattern)
            and getattr(statement, 'action', None)
            and statement.action.__name__ == 'install_image_failing'
        )
        self.assertIsNotNone(re.search(
            install_failure_statement.pattern,
            'FAILED: install_add  exit(1)',
        ))

        expected_execute_call = [call('install add file bootflash:/image.bin activate commit prompt-level none', reply=reload_dialog, append_error_pattern=['FAILED:'], timeout=500),
                                call('more bootflash:packages.conf'),
                                call('install add file bootflash:/image.bin activate commit prompt-level none', reply=reload_dialog, append_error_pattern=['FAILED:'], timeout=500),
                                call('install commit')]

        device.execute.assert_has_calls(expected_execute_call)
        expected_reload_call = call(
                '',
                reload_creds='default',
                prompt_recovery=True,
                error_pattern=['FAILED:.*?$'],
                device_recovery=False,
                timeout=500,
                reply=reload_dialog,
            )
        device.reload.assert_has_calls([expected_reload_call])
        device.api.free_up_disk_space.assert_called_with(
            destination='', required_size=466067456,
            protected_files=['image.bin'], allow_deletion_failure=True,
            skip_deletion=False)
        device.api.collect_install_log.assert_not_called()
        device.api.get_running_image.assert_called_once()
        self.assertEqual(Passed, steps.details[0].result)

    def test_iosxe_install_image_skip(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        device = Mock()
        device.parse = Mock(return_value={
                                 'location': {
                                     'Switch 1': {
                                         'pkg_state': {
                                             1: {'type': 'IMG',
                                                 'state': 'C',
                                                 'filename_version': '17.17.01.0.207986'}},
                                         'auto_abort_timer': 'inactive'
                                         }}})

        device.api.get_running_image.return_value = 'sftp://server/image.bin'
        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])
        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Skipped, steps.details[1].result)

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_iosxe_install_image_grub_boot_image(self, dialog):
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.reload = Mock()
        device.parse = Mock(return_value={
                                 'location': {
                                     'Switch 1': {
                                         'pkg_state': {
                                             1: {'type': 'IMG',
                                                 'state': 'C',
                                                 'filename_version': '17.17.01.0.207986'}},
                                         'auto_abort_timer': 'inactive'
                                         }}})

        device.api.get_running_image = Mock()

        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'],
                          reload_service_args=dict(grub_boot_image='packages.conf'))

        expected_execute_call = [call('install add file sftp://server/image.bin activate commit prompt-level none',
                                 reply=reload_dialog,
                                 append_error_pattern=['FAILED:'],
                                 timeout=500),
                                 call('install commit')]

        device.execute.assert_has_calls(expected_execute_call)
        expected_reload_call = call(
                '',
                reload_creds='default',
                prompt_recovery=True,
                error_pattern=['FAILED:.*?$'],
                device_recovery=False,
                grub_boot_image='packages.conf',
                timeout=500,
                reply=reload_dialog,
            )
        device.reload.assert_has_calls([expected_reload_call])
        self.assertEqual(Passed, steps.details[0].result)

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_install_image_fail(self, dialog):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()

        device = Mock()
        device.api = Mock()
        device.reload = Mock()
        device.spawn = Mock()
        device.context = {}
        device.parse = Mock(return_value={
            'location': {
                'Switch 1': {
                    'pkg_state': {
                        1: {'type': 'IMG',
                            'state': 'U',
                            'filename_version': '17.17.01.0.207986'}},
                    'auto_abort_timer': 'inactive'
                }}})

        device.api.get_running_image = Mock()
        # The device recovery/diagnostic collection is owned by the
        # collect_install_log API and covered by its own SDK API tests, so
        # only the stage's contract with that API is asserted here.
        device.api.collect_install_log = Mock()

        device.clean_space = None
        device.issu_in_progress = None
        device.connections = {'telnet': True}
        device.default_connection_alias = 'ssh'

        device.execute = Mock(side_effect=[
            "SUCCESS:",  # install commit
            Exception(
                "FAILED: Install Operation failed as one "
                "or more package file(s) for running "
                "image is not present in the device"
            ),  # install add file
        ])

        # Run the install_image method
        with self.assertRaises(TerminateStepSignal):
            cls.install_image(
                steps=steps, device=device, images=['/image/stay-isr-image.bin']
            )

        # The stage must delegate connection recovery to the API instead of
        # driving the state machine itself.
        device.api.collect_install_log.assert_called_once_with(
            reconnect=True, reconnect_timeout=150)

        # Verify the steps reflect the failure
        assert steps.details[0].name == (
            'Check for previous uncommitted install operation'
        )
        assert steps.details[1].name == (
            "Installing image '/image/stay-isr-image.bin'"
        )
        assert steps.details[0].result == Passed
        assert steps.details[1].result == Failed

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_install_image_empty_output(self, dialog):
        """Test that install fails when output is empty or None"""
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.name = 'test_device'
        device.spawn = Mock()
        device.parse = Mock(return_value={
            'location': {
                'Switch 1': {
                    'pkg_state': {
                        1: {'type': 'IMG', 'state': 'C', 'filename_version': '17.17.01.0.207986'}
                    },
                    'auto_abort_timer': 'inactive'
                }
            }
        })

        # Mock execute to return empty output
        # Note: Only the install command calls execute in this path
        device.execute = Mock(return_value='')
        device.api.get_running_image = Mock(return_value='old_image.bin')
        device.api.collect_install_log = Mock()

        with self.assertRaises(TerminateStepSignal):
            cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])

        # Verify the install failed
        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Failed, steps.details[1].result)

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_install_timeout_collects_logs_with_reconnect(self, dialog):
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()

        device = create_test_device('PE1', os='iosxe')
        device.name = 'PE1'
        device.spawn = Mock(buffer='Username:')
        device.parse = Mock(return_value={})

        install_cmd = (
            'install add file bootflash:/image.bin '
            'activate commit prompt-level none'
        )

        def _execute(command, **kwargs):
            if command == install_cmd:
                raise UniconTimeoutError('install operation timed out')
            return ''

        device.execute = Mock(side_effect=_execute)
        device.api.get_running_image = Mock(return_value='old-image.bin')
        device.api.collect_install_log = Mock()

        with self.assertRaises(TerminateStepSignal):
            cls.install_image(
                steps=steps,
                device=device,
                images=['bootflash:/image.bin'],
            )

        # The stage must delegate resynchronization/reconnect and enable
        # recovery to the collect_install_log API rather than handling it
        # locally.
        device.api.collect_install_log.assert_called_once_with(
            reconnect=True, reconnect_timeout=150)
        self.assertEqual(Failed, steps.details[1].result)

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_install_timeout_preserves_failure_when_log_collection_fails(
            self, dialog):
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()

        device = create_test_device('PE1', os='iosxe')
        device.name = 'PE1'
        device.spawn = Mock(buffer='Username:')
        device.parse = Mock(return_value={})
        install_timeout = UniconTimeoutError('install operation timed out')
        device.execute = Mock(side_effect=install_timeout)
        device.api.get_running_image = Mock(return_value='old-image.bin')
        device.api.collect_install_log = Mock(side_effect=RuntimeError(
            'device did not reach enable mode'))

        with self.assertRaises(TerminateStepSignal):
            cls.install_image(
                steps=steps,
                device=device,
                images=['bootflash:/image.bin'],
            )

        # A failure while collecting diagnostics must not mask the
        # original install error.
        device.api.collect_install_log.assert_called_once_with(
            reconnect=True, reconnect_timeout=150)
        failure_reason = steps.details[1].result.reason
        self.assertIn(
            'diagnostic collection also failed',
            failure_reason,
        )
        self.assertIn('device did not reach enable mode', failure_reason)
        self.assertIn('install operation timed out', failure_reason)
        self.assertEqual(Failed, steps.details[1].result)


class TestVerifyRunningImage(unittest.TestCase):

    def setUp(self):
        self.cls = InstallImage()
        self.device = create_test_device('PE1', os='iosxe', platform='cat9k')

    def test_iosxe_verify_running_image_skipped(self):

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'show version': '''
Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]
Copyright (c) 1986-2011 by Cisco Systems, Inc.
Compiled Wed 15-Jun-11 08:54 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2011 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
ROM: Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]

issu-asr-lns uptime is 1 hour, 16 minutes
Uptime for this control processor is 1 hour, 17 minutes
System returned to ROM by reload
System image file is "flash:/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin"
Last reload reason: Reload Command



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

cisco ASR1006 (RP2) processor with 4254354K/6147K bytes of memory.
3 ATM interfaces
32768K bytes of non-volatile configuration memory.
8388608K bytes of physical memory.
1826815K bytes of eUSB flash at bootflash:.
78085207K bytes of SATA hard disk at harddisk:.

Configuration register is 0x1
                    '''
                }

            def __call__(self, cmd, *args, **kwargs):
                output = self.data.get(cmd)
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        self.cls.history = OrderedDict()
        self.cls.mock_value = OrderedDict()
        setattr(self.cls.mock_value, 'parameters', {})
        self.cls.history.update({'InstallImage': self.cls.mock_value})
        self.cls.history['InstallImage'].parameters =  OrderedDict()
        with self.assertRaises(AEtestSkippedSignal):
            self.cls.verify_running_image(steps=steps,
                                          device=self.device,
                                          images=['/path/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin']
            )

        self.assertEqual(Skipped, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('show version')
        ])

        self.assertEqual(self.cls.history['InstallImage'].parameters['image_mapping'],
                         {'/path/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin':
                          'flash:/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin'})

    def test_iosxe_verify_running_image_passx(self):

        class MockExecute:
            def __init__(self, *args, **kwargs):
                self.data = {
                    'show version': '''
Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]
Copyright (c) 1986-2011 by Cisco Systems, Inc.
Compiled Wed 15-Jun-11 08:54 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2011 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
ROM: Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]

issu-asr-lns uptime is 1 hour, 16 minutes
Uptime for this control processor is 1 hour, 17 minutes
System returned to ROM by reload
System image file is "flash:/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin"
Last reload reason: Reload Command



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

cisco ASR1006 (RP2) processor with 4254354K/6147K bytes of memory.
3 ATM interfaces
32768K bytes of non-volatile configuration memory.
8388608K bytes of physical memory.
1826815K bytes of eUSB flash at bootflash:.
78085207K bytes of SATA hard disk at harddisk:.

Configuration register is 0x1
                    '''
                }

            def __call__(self, cmd, *args, **kwargs):
                output = self.data.get(cmd)
                return output
           

        mock_execute = MockExecute()
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        self.cls.history = OrderedDict()
        self.cls.mock_value = OrderedDict()
        setattr(self.cls.mock_value, 'parameters', {})
        self.cls.history.update({'InstallImage': self.cls.mock_value})
        self.cls.history['InstallImage'].parameters =  OrderedDict()

        self.cls.verify_running_image(steps=steps,
                                      device=self.device,
                                      images=['/path/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044520.SSA.bin']
                                      )

        self.assertEqual(Passx, steps.details[0].result)


class TestVerifyRunningImage(unittest.TestCase):

    def test_iosxe_unconfigure_and_verify_ignore_startup_config(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        device = Mock()
        device.api.unconfigure_ignore_startup_config = Mock()
        device.api.verify_ignore_startup_config = Mock(return_value=False)

        cls.unconfigure_startup_config(steps=steps, device=device)
        cls.verify_ignore_startup_config(steps=steps, device=device)

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Passed, steps.details[1].result)

class TestConfigureBootManual(unittest.TestCase):

    def test_iosxe_boot_manual_pass(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        device = Mock()
        device.api.no_boot_manual = Mock()

        cls.configure_no_boot_manual(steps=steps,
                                    device=device)

        self.assertEqual(Passed, steps.details[0].result)
        device.api.configure_no_boot_manual.assert_called_once()

    def test_iosxe_boot_manual_passx(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        device = Mock()
        device.api.configure_no_boot_manual = Mock(side_effect=Exception)

        cls.configure_no_boot_manual(steps=steps,
                                    device=device)
        self.assertEqual(Passx, steps.details[0].result)
        device.api.configure_no_boot_manual.assert_called_once()


class VerifyInstallSpace(unittest.TestCase):

    IMAGE = 'flash:/ie3x00-universalk9.SSA.bin'
    IMAGE_SIZE = 457558593
    RUNNING_IMAGE = 'flash:ie3x00-universalk9.OLD.SSA.bin'

    def setUp(self):
        self.cls = InstallImage()
        self.cls.history = MagicMock()

        self.device = Mock()
        self.device.name = 'PE1'
        self.device.is_ha = False
        self.device.api.get_file_size = Mock(return_value=self.IMAGE_SIZE)
        self.device.api.get_platform_default_dir = Mock(return_value='flash:')
        self.device.api.get_running_image = Mock(return_value=self.RUNNING_IMAGE)
        self.device.api.free_up_disk_space = Mock(return_value=True)

    def test_pass_when_enough_space(self):
        steps = Steps()
        # 1.3x the image size, above the 1.25 default
        self.device.api.get_available_space = Mock(
            return_value=int(self.IMAGE_SIZE * 1.3))

        self.cls.verify_install_space(
            steps=steps, device=self.device, images=[self.IMAGE])

        self.assertEqual(Passed, steps.details[0].result)
        self.device.api.free_up_disk_space.assert_not_called()

    def test_frees_space_using_padded_requirement(self):
        steps = Steps()
        # 1.03x the image size clears the device precheck but not expansion
        self.device.api.get_available_space = Mock(
            return_value=int(self.IMAGE_SIZE * 1.03))

        with patch('genie.libs.clean.stages.iosxe.stages.get_protected_files',
                   return_value=['ie3x00-universalk9.SSA.bin']):
            self.cls.verify_install_space(
                steps=steps, device=self.device, images=[self.IMAGE])

        self.assertEqual(Passed, steps.details[0].result)
        self.device.api.free_up_disk_space.assert_called_once_with(
            destination='flash:',
            required_size=int(self.IMAGE_SIZE * 1.25),
            protected_files=ANY,
            allow_deletion_failure=True,
            skip_deletion=False)

    def test_honours_custom_space_factor(self):
        steps = Steps()
        self.device.api.get_available_space = Mock(return_value=0)

        with patch('genie.libs.clean.stages.iosxe.stages.get_protected_files',
                   return_value=[]):
            self.cls.verify_install_space(
                steps=steps, device=self.device, images=[self.IMAGE],
                install_space_factor=1.5)

        self.assertEqual(
            int(self.IMAGE_SIZE * 1.5),
            self.device.api.free_up_disk_space.call_args.kwargs['required_size'])

    def test_protects_running_image(self):
        steps = Steps()
        self.device.api.get_available_space = Mock(return_value=0)

        # packages.conf is absent in bundle mode, so this returns None
        with patch('genie.libs.clean.stages.iosxe.stages.get_protected_files',
                   return_value=None):
            self.cls.verify_install_space(
                steps=steps, device=self.device, images=[self.IMAGE])

        protected = self.device.api.free_up_disk_space.call_args.kwargs[
            'protected_files']
        self.assertIn('ie3x00-universalk9.OLD.SSA.bin', protected)
        self.assertIn('ie3x00-universalk9.SSA.bin', protected)

    def test_passx_when_space_cannot_be_freed(self):
        steps = Steps()
        self.device.api.get_available_space = Mock(return_value=0)
        self.device.api.free_up_disk_space = Mock(return_value=False)

        with patch('genie.libs.clean.stages.iosxe.stages.get_protected_files',
                   return_value=[]):
            self.cls.verify_install_space(
                steps=steps, device=self.device, images=[self.IMAGE])

        self.assertEqual(Passx, steps.details[0].result)

    def test_passx_when_free_up_disk_space_raises(self):
        steps = Steps()
        self.device.api.get_available_space = Mock(return_value=0)
        self.device.api.free_up_disk_space = Mock(side_effect=Exception)

        with patch('genie.libs.clean.stages.iosxe.stages.get_protected_files',
                   return_value=[]):
            self.cls.verify_install_space(
                steps=steps, device=self.device, images=[self.IMAGE])

        self.assertEqual(Passx, steps.details[0].result)

    def test_skipped_when_image_size_unknown(self):
        steps = Steps()
        self.device.api.get_file_size = Mock(return_value=None)

        self.cls.verify_install_space(
            steps=steps, device=self.device, images=[self.IMAGE])

        self.assertEqual(Skipped, steps.details[0].result)
        self.device.api.free_up_disk_space.assert_not_called()

    def test_skipped_when_default_dir_unavailable(self):
        steps = Steps()
        self.device.api.get_platform_default_dir = Mock(side_effect=Exception)

        self.cls.verify_install_space(
            steps=steps, device=self.device, images=[self.IMAGE])

        self.assertEqual(Skipped, steps.details[0].result)
        self.device.api.free_up_disk_space.assert_not_called()

    def test_ha_falls_through_when_any_directory_returns_none(self):
        steps = Steps()
        self.device.is_ha = True
        self.device.api.get_platform_default_dir = Mock(
            return_value=['flash:', 'stby-flash:'])
        # Active RP has plenty of space, standby returns None (unknown).
        self.device.api.get_available_space = Mock(
            side_effect=[int(self.IMAGE_SIZE * 2), None])

        with patch('genie.libs.clean.stages.iosxe.stages.get_protected_files',
                   return_value=[]):
            self.cls.verify_install_space(
                steps=steps, device=self.device, images=[self.IMAGE])

        # Should NOT pass — must fall through to free_up_disk_space.
        self.device.api.free_up_disk_space.assert_called_once()
