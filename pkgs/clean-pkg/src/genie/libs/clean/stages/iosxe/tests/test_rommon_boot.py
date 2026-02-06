import unittest

from unittest import mock
from unittest.mock import MagicMock, Mock, call
from unicon.eal.dialogs import Statement
from ipaddress import IPv4Address, IPv6Address, IPv4Interface, IPv6Interface

from pyats.results import Passed, Failed
from pyats.aetest.steps import Steps
from pyats.aetest.signals import TerminateStepSignal

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.clean.stages.iosxe.stages import RommonBoot
from genie.libs.clean.exception import FailedToBootException

RESULT_METHODS = ['passed', 'failed', 'skipped', 'passx', 'blocked', 'errored', 'aborted']


class TestRommonBoot(unittest.TestCase):

    def setUp(self):
        self.cls = RommonBoot()
        self.device = create_test_device(
            name='aDevice', os='iosxe')

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

    def test_go_to_rommon(self):
        steps = mock.MagicMock()
        self.device.rommon = mock.Mock()
        self.cls.go_to_rommon(steps, self.device, config_register="0x40")
        steps.start.assert_called_with("Bring device down to rommon mode")
        self.device.rommon.assert_called_once()

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

    @mock.patch('genie.libs.clean.recovery.iosxe.recovery.device_recovery')
    def test_rommon_boot(self, device_recovery):
        steps = mock.MagicMock()
        recovery_info = {'timeout': 100, 'golden_image': ['GOLDEN IMAGE']}
        device_recovery.return_value = recovery_info
        self.device.clean = {'device_recovery': recovery_info}
        self.device.rommon = mock.Mock()
        self.device.rommon()
        self.device.is_ha = mock.Mock()
        self.device.default = mock.Mock()
        self.device.state_machine = mock.Mock()
        self.device.default.state_machine.current_state = 'rommon'
        self.cls.rommon_boot(steps, self.device, image=['GOLDEN IMAGE'],timeout=100,
                             grub_activity_pattern='The highlighted entry will be (?:booted|executed) automatically')
        steps.start.assert_called_with("Boot device from rommon")
        self.device.rommon.assert_called_once()

    @mock.patch('genie.libs.clean.stages.iosxe.stages.time.sleep')
    def test_rommon_boot_tftp_retry_success_on_second_attempt(self, mock_sleep):
        """Test that TFTP rommon boot succeeds on the second attempt after one failure"""
        steps = mock.MagicMock()
        recovery_info = {
            'timeout': 100, 
            'golden_image': [], 
            'tftp_boot': {
                'ip_address': ['10.1.1.1'],
                'subnet_mask': '255.255.255.0',
                'gateway': '10.1.1.254',
                'tftp_server': '10.1.1.100'
            }
        }
        self.device.clean = {'device_recovery': recovery_info}
        self.device.is_ha = False
        self.device.default = mock.Mock()
        self.device.default.state_machine = mock.Mock()
        self.device.default.state_machine.current_state = 'rommon'

        # Mock the API call - fail once, succeed on second attempt
        self.device.api.device_rommon_boot = mock.Mock(
            side_effect=[FailedToBootException('TFTP timeout'), None]
        )

        # Pass the retry parameters as kwargs
        self.cls.rommon_boot(
            steps=steps, 
            device=self.device,
            timeout=100,
            tftp_boot_max_attempts=3,
            tftp_boot_sleep_interval=10
        )

        # Verify retry happened
        assert self.device.api.device_rommon_boot.call_count == 2
        mock_sleep.assert_called_once_with(10)

        step_context = steps.start.return_value.__enter__.return_value
        # Should not fail since it succeeded on second attempt
        step_context.failed.assert_not_called()

    @mock.patch('genie.libs.clean.stages.iosxe.stages.time.sleep')
    def test_rommon_boot_tftp_retry_all_attempts_fail(self, mock_sleep):
        """Test that TFTP rommon boot fails after exhausting all retry attempts"""
        steps = mock.MagicMock()
        recovery_info = {
            'timeout': 100, 
            'golden_image': [], 
            'tftp_boot': {
                'ip_address': ['10.1.1.1'],
                'subnet_mask': '255.255.255.0',
                'gateway': '10.1.1.254',
                'tftp_server': '10.1.1.100'
            }
        }
        self.device.clean = {'device_recovery': recovery_info}
        self.device.is_ha = False
        self.device.default = mock.Mock()
        self.device.default.state_machine = mock.Mock()
        self.device.default.state_machine.current_state = 'rommon'

        # All attempts fail
        test_exception = FailedToBootException('TFTP timeout')
        self.device.api.device_rommon_boot = mock.Mock(side_effect=test_exception)

        # Pass the retry parameters as kwargs
        self.cls.rommon_boot(
            steps=steps, 
            device=self.device,
            timeout=100,
            tftp_boot_max_attempts=3,
            tftp_boot_sleep_interval=10
        )

        # Verify all retry attempts were made
        assert self.device.api.device_rommon_boot.call_count == 3
        assert mock_sleep.call_count == 2  # Sleep between attempts, not after last one

        step_context = steps.start.return_value.__enter__.return_value
        # Should fail with appropriate message
        step_context.failed.assert_called_once()
