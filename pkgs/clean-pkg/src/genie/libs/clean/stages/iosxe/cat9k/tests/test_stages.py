import unittest

from unittest import mock

from unicon.eal.dialogs import Statement
from pyats.topology.credentials import Credentials

from pyats.results import Passed, Failed
from pyats.aetest.steps import Steps
from pyats.aetest.signals import TerminateStepSignal

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.clean.stages.iosxe.stages import RommonBoot


RESULT_METHODS = ['passed', 'failed', 'skipped', 'passx', 'blocked', 'errored', 'aborted']


class TestRommonBoot(unittest.TestCase):

    def setUp(self):
        self.cls = RommonBoot()
        self.device = create_test_device(
            name='aDevice', os='iosxe', platform='cat9k')

    def test_delete_boot_variables_pass(self):
        steps = mock.MagicMock()
        self.device.configure = mock.Mock()

        self.cls.delete_boot_variables(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Delete configured boot variables")

        # Verify the config command was ran
        self.device.configure.assert_called_with("no boot system")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    def test_delete_boot_variables_fail(self):
        steps = mock.MagicMock()
        config_exception = Exception()

        self.device.configure = mock.Mock(side_effect=config_exception)

        self.cls.delete_boot_variables(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Delete configured boot variables")

        # Verify the config command was ran
        self.device.configure.assert_called_with("no boot system")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            'Failed to delete configured boot variables',
            from_exception=config_exception)

    def test_write_memory_pass(self):
        steps = mock.MagicMock()
        self.device.api.execute_write_memory = mock.Mock()
        self.device.execute = mock.Mock()

        self.cls.write_memory(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Write memory")

        # Verify the api was called
        self.device.api.execute_write_memory.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    def test_write_memory_fail(self):
        steps = mock.MagicMock()
        api_exception = Exception()
        self.device.api.execute_write_memory = mock.Mock(side_effect=api_exception)
        self.device.execute = mock.Mock()

        self.cls.write_memory(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Write memory")

        # Verify the api was called
        self.device.api.execute_write_memory.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            "Failed to write memory",
            from_exception=api_exception)

    def test_go_to_rommon_pass(self):
        """Test that go_to_rommon correctly calls the device rommon method"""
        steps = mock.MagicMock()
        self.device.rommon = mock.Mock()
        self.device.is_ha = False

        self.cls.go_to_rommon(steps=steps, device=self.device)

        steps.start.assert_called_with("Bring device down to rommon mode")


        self.device.rommon.assert_called_once()

        step_context = steps.start.return_value.__enter__.return_value
        for result in RESULT_METHODS:
            if result != 'passed':
                getattr(step_context, result).assert_not_called()

    def test_rommon_boot_pass(self):
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.api.device_rommon_boot = mock.Mock()
        self.device.is_ha = False

        self.cls.rommon_boot(
            steps=steps, device=self.device, image=['bootflash:/test.bin'])

        steps.start.assert_called_with("Boot device from rommon")
        self.device.api.device_rommon_boot.assert_called_once()

    def test_rommon_boot_fail_abstraction_lookup(self):
        """Test that the stage correctly handles a failure from the boot API"""
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False

        api_exception = Exception("Boot API Failed")
        self.device.api.device_rommon_boot = mock.Mock(side_effect=api_exception)

        self.cls.rommon_boot(
            steps=steps,
            device=self.device,
            image=['bootflash:/test.bin']
        )

        self.device.api.device_rommon_boot.assert_called_once()

        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            "Failed to boot the device from rommon",
            from_exception=api_exception
        )


    def test_rommon_boot_fail_recovery_worker(self):
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False

        api_exception = Exception("Boot failed")
        self.device.api.device_rommon_boot = mock.Mock(side_effect=api_exception)

        self.cls.rommon_boot(
            steps=steps, device=self.device, image=['bootflash:/test.bin'])

        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            "Failed to boot the device from rommon",
            from_exception=api_exception)

    @mock.patch('genie.libs.clean.stages.iosxe.stages._disconnect_reconnect')
    def test_reconnect_pass(self, _disconnect_reconnect):
        steps = mock.MagicMock()
        _disconnect_reconnect.return_value = True

        self.cls.reconnect(steps=steps, device=self.device)

        steps.start.assert_called_with("Reconnect to device")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    @mock.patch('genie.libs.clean.stages.iosxe.stages._disconnect_reconnect')
    def test_reconnect_fail(self, _disconnect_reconnect):
        steps = mock.MagicMock()
        _disconnect_reconnect.return_value = False

        self.cls.reconnect(steps=steps, device=self.device)

        steps.start.assert_called_with("Reconnect to device")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with("Failed to reconnect")

    def test_rommon_boot_tftp_with_retry_params(self):
        """Test that TFTP boot retry parameters are passed to the API"""
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.api.device_rommon_boot = mock.Mock()
        self.device.is_ha = False
        self.device.clean = {}

        mock_testbed = mock.MagicMock()
        mock_testbed.credentials = Credentials()
        self.device.testbed = mock_testbed

        self.device.management = {
            'address': {
                'ipv4': mock.MagicMock(ip='10.1.1.1', netmask='255.255.255.0')
            },
            'gateway': {'ipv4': '10.1.1.254'}
        }

        self.device.testbed.servers = {'tftp': {'address': '10.1.1.100'}}

        tftp_config = {'image': ['test.bin']}

        self.cls.rommon_boot(
            steps=steps,
            device=self.device,
            tftp=tftp_config,
            tftp_boot_max_attempts=5,
            tftp_boot_sleep_interval=45
        )

        # Verify that device_rommon_boot was called with the expected parameters
        self.device.api.device_rommon_boot.assert_called_once()
        call_kwargs = self.device.api.device_rommon_boot.call_args.kwargs

        # Check that key parameters are present
        self.assertIn('tftp_boot', call_kwargs)
        self.assertEqual(call_kwargs['golden_image'], None)
        self.assertIn('grub_activity_pattern', call_kwargs)
        self.assertIn('timeout', call_kwargs)
        
        passed_tftp = call_kwargs['tftp_boot']
        self.assertEqual(passed_tftp['image'], ['test.bin'])
