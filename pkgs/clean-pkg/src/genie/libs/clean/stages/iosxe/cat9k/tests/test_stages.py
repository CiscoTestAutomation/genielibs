import unittest

from unittest import mock

from unicon.eal.dialogs import Statement

from pyats.results import Passed, Failed
from pyats.aetest.steps import Steps
from pyats.aetest.signals import TerminateStepSignal

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.clean.stages.iosxe.cat9k.stages import RommonBoot


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

    @mock.patch('genie.libs.clean.stages.iosxe.cat9k.stages.Statement')
    @mock.patch('genie.libs.clean.stages.iosxe.cat9k.stages.Dialog')
    def test_go_to_rommon_pass(self, dialog, statement):
        steps = mock.MagicMock()
        self.device.sendline = mock.Mock()
        self.device.spawn = mock.Mock()
        self.device.is_ha = False
        self.device.subconnections = mock.MagicMock()
        self.device.expect = mock.Mock()
        self.device.destroy_all = mock.Mock()

        reload_dialog = mock.Mock()
        dialog.return_value = reload_dialog

        self.cls.go_to_rommon(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Bring device down to rommon mode")

        statement.assert_has_calls([
            mock.call(pattern=r".*System configuration has been modified\. Save\? \[yes\/no\].*",
                      action='sendline(yes)',
                      loop_continue=True,
                      continue_timer=False),
            mock.call(pattern=r".*Proceed with reload\? \[confirm\].*",
                      action='sendline()',
                      loop_continue=False,
                      continue_timer=False)
        ])

        self.device.sendline.assert_called_with("reload")
        reload_dialog.process.assert_called_with(self.device.spawn)
        self.device.expect.assert_called_with(
            ['(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)'], timeout=60)

        self.device.destroy_all.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    @mock.patch('genie.libs.clean.stages.iosxe.cat9k.stages.pcall')
    def test_rommon_boot_pass(self, pcall):
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False
        self.device.start = 'telnet 127.0.0.1 0000'

        self.cls.rommon_boot(
            steps=steps, device=self.device, image='bootflash:/test.bin')

        steps.start.assert_called_with("Boot device from rommon")
        self.device.instantiate.assert_called_once()

        pcall.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    @mock.patch('genie.libs.clean.stages.iosxe.cat9k.stages.Lookup')
    def test_rommon_boot_fail_abstraction_lookup(self, lookup):
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False
        self.device.start = 'telnet 127.0.0.1 0000'
        lookup_exception = Exception()
        lookup.from_device.side_effect = lookup_exception

        self.cls.rommon_boot(
            steps=steps, device=self.device, image='bootflash:/test.bin')

        steps.start.assert_called_with("Boot device from rommon")
        self.device.instantiate.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_any_call("Abstraction lookup failed",
                                               from_exception=lookup_exception)


    @mock.patch('genie.libs.clean.stages.iosxe.cat9k.stages.pcall')
    def test_rommon_boot_fail_recovery_worker(self, pcall):
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False
        self.device.start = 'telnet 127.0.0.1 0000'
        pcall_exception = Exception()
        pcall.side_effect = pcall_exception

        self.cls.rommon_boot(
            steps=steps, device=self.device, image='bootflash:/test.bin')

        steps.start.assert_called_with("Boot device from rommon")
        self.device.instantiate.assert_called_once()

        pcall.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            "Failed to boot the device from rommon",
            from_exception=pcall_exception)

    @mock.patch('genie.libs.clean.stages.iosxe.cat9k.stages._disconnect_reconnect')
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

    @mock.patch('genie.libs.clean.stages.iosxe.cat9k.stages._disconnect_reconnect')
    def test_reconnect_fail(self, _disconnect_reconnect):
        steps = mock.MagicMock()
        _disconnect_reconnect.return_value = False

        self.cls.reconnect(steps=steps, device=self.device)

        steps.start.assert_called_with("Reconnect to device")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with("Failed to reconnect")
