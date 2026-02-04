import logging
import unittest
import re
from unittest.mock import Mock, MagicMock, call, ANY, patch, PropertyMock
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.stages import InstallImage
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.easypy import runtime
from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped, Passx
from pyats.aetest.signals import TerminateStepSignal, AEtestSkippedSignal, AEtestStepPassxSignal


import unicon
from unicon.eal.dialogs import Statement, Dialog

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

        def mock_execute(*args, **kwargs):
            assert args == ('puts [open "bootflash:/packages.conf" w+] {}',)

        self.device.tclsh = mock_execute

        # And we want the execute_set_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.api.execute_set_boot_variable = Mock()
        self.device.api.unconfigure_ignore_startup_config = Mock()
        # Call the method to be tested (clean step inside class)
        self.cls.set_boot_variable(
            steps=steps, device=self.device
        )
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

        def mock_execute(*args, **kwargs):
            assert args == ('puts [open "bootflash:/packages.conf" w+] {}',)

        self.device.tclsh = mock_execute

        # And we want the execute_set_boot_variable api to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_set_boot_variable = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.set_boot_variable(
                steps=steps, device=self.device
            )

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

        def mock_execute(*args, **kwargs):
            assert args == ('puts [open "bootflash:/packages.conf" w+] {}',)

        self.device.tclsh = mock_execute

        # And we want the execute_set_boot_variable
        self.device.api.execute_set_boot_variable = Mock()
        
        self.device.api.unconfigure_ignore_startup_config= Mock(side_effect=Exception)
        
        self.cls.set_boot_variable(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Passx, steps.details[0].result)

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
        self.device.api.verify_ignore_startup_config = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.verify_boot_variable(
            steps=steps, device=self.device
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        
    def test_verify_ignore_config_fail(self):
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
        self.device.api.verify_ignore_startup_config = Mock(return_value=False)

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_boot_variable(
                steps=steps, device=self.device)
        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

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

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the fail case.
        self.device.execute = Mock(return_value=data1['show boot'])

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

    def test_verify_ignore_config_exception(self):
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
        self.device.api.verify_ignore_startup_config = Mock(side_effect=Exception)

        # Call the method to be tested (clean step inside class)
        self.cls.verify_boot_variable(
                steps=steps, device=self.device)
        # Check the overall result is as expected
        self.assertEqual(Passx, steps.details[0].result)


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
                                 error_pattern=['FAILED:'],
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
    def test_iosxe_install_image_pass_retries_not_enough_space(self, dialog):
        reload_dialog = Mock()
        dialog.return_value = reload_dialog
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'
        
        package_data = '''boot   rp 0 0   rp_boot cat9k.pkg
boot   rp 1 0   rp_boot cat9k-1.pkg
iso   rp 0 0   rp_base cat9k-2.pkg'''
        
        device = create_test_device('PE1', os='iosxe')
        device.reload = Mock()
        device.space_required = 5
        device.spawn = Mock()
        device.clean_space = True
        device.is_ha = False
        device.execute = Mock(side_effect=[Exception('Not enough space'),'Directory of bootflash:/',package_data,"bootflash", "", ""])
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

        expected_execute_call = [call('install add file bootflash:/image.bin activate commit prompt-level none', reply=reload_dialog, error_pattern=['FAILED:'], timeout=500),
                                call('more bootflash:packages.conf'),
                                call('install add file bootflash:/image.bin activate commit prompt-level none', reply=reload_dialog, error_pattern=['FAILED:'], timeout=500),
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
        device.api.free_up_disk_space.assert_called_with(destination='', required_size=5000,
                                                         protected_files=['image.bin'], allow_deletion_failure=True, skip_deletion=False)
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
                                 error_pattern=['FAILED:'],
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
    @patch('genie.libs.sdk.apis.iosxe.support.tech_support.get_default_dir')
    @patch('genie.libs.sdk.apis.iosxe.support.tech_support.datetime')
    def test_install_image_fail(self, mock_datetime, mock_get_default_dir, dialog):
        mock_get_default_dir.return_value = "flash:"
        mock_datetime.utcnow.return_value.strftime.return_value = '20250101T000000000'
        with patch.object(type(runtime), 'directory', new_callable=PropertyMock) as mock_dir:
            mock_dir.return_value = "/tmp"

            steps = Steps()
            cls = InstallImage()
            cls.history = MagicMock()

            device = Mock()
            device.api = Mock()
            device.reload = Mock()
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
            device.api.copy_from_device = Mock()
            import types
            from genie.libs.sdk.apis.iosxe.support.tech_support import collect_install_log
            device.api.collect_install_log = types.MethodType(collect_install_log, device)

            device.clean_space = None
            device.issu_in_progress = None
            device.connections = {'telnet': True}
            device.default_connection_alias = 'ssh'

            # Provide outputs for all expected calls
            device.execute = Mock(side_effect=[
                "SUCCESS:",  # install commit
                Exception("FAILED: Install Operation failed as one or more package file(s) for running image is not present in the device"),  # install add file
                "output for current detail",  # show platform software install-manager switch active R0 operation current detail
                "output for history detail",  # show platform software install-manager switch active R0 operation history detail
                "output for tech-support",    # show tech-support install | append show_tech_support.txt
                "Done with creation of the archive file:[flash:archive.tar.gz]",  # request platform software trace archive
                "flash:" # dir
            ])

            with patch('genie.libs.sdk.apis.iosxe.support.tech_support.re.search') as mock_search:
                mock_match = MagicMock()
                mock_match.group.return_value = "flash:archive.tar.gz"
                mock_search.return_value = mock_match

                # Run the install_image method
                with self.assertRaises(TerminateStepSignal):
                    cls.install_image(
                        steps=steps, device=device, images=['/image/stay-isr-image.bin']
                    )

            # Assert all expected calls inside collect_install_log
            device.execute.assert_any_call("show platform software install-manager r0 operation current detail")
            device.execute.assert_any_call("show platform software install-manager r0 operation history detail")
            device.execute.assert_any_call("show tech-support install | append show_tech_support_20250101T000000.txt", timeout=600)
            device.execute.assert_any_call("request platform software trace archive")
            device.api.copy_from_device.assert_any_call(local_path="flash:show_tech_support_20250101T000000.txt", remote_path="/tmp")
            device.api.copy_from_device.assert_any_call(local_path="flash:archive.tar.gz", remote_path="/tmp")

            # Verify the steps reflect the failure
            assert steps.details[0].name == 'Check for previous uncommitted install operation'
            assert steps.details[1].name == "Installing image '/image/stay-isr-image.bin'"
            assert steps.details[0].result == Passed
            assert steps.details[1].result == Failed


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

    def test_iosxe_configure_and_verify_ignore_startup_config(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        device = Mock()
        device.api.unconfigure_ignore_startup_config = Mock()
        device.api.verify_ignore_startup_config = False

        cls.configure_and_verify_startup_config(steps=steps,
                                                device=device)

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Passx, steps.details[1].result)

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