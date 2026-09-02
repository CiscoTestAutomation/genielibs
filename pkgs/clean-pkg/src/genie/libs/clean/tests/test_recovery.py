import unittest
from functools import partial
from unittest.mock import Mock, MagicMock, patch

from unicon import Connection
from unicon.settings import Settings

from pyats import aetest
from pyats.aetest import processors
from pyats.aetest.base import TestItem as AEtestTestItem
from pyats.aetest.processors.handler import ProcessorHandler
from pyats.aetest.signals import (
    AEtestFailedSignal,
    AEtestPassedSignal,
    AEtestPassxSignal,
)
from pyats.aetest.processors.signals import (
    ProcessorErroredSignal,
    ProcessorFailedSignal,
    ProcessorPassedSignal,
    ProcessorPassxSignal,
)
from pyats.aetest.steps import Steps
from pyats.results import Blocked, Errored, Failed, Passed, Passx, Skipped

from genie.libs.clean.recovery.recovery import recovery_processor

import logging

logger = logging.getLogger(__name__)


class MockDisconnectReconnect:

    def __init__(self, *args, **kwargs):
        self.state = iter([False, True, False, False, False])

    def __call__(self, *arg, **kwargs):
        state = next(self.state)
        return state


mock_disconnect_reconnect =  MockDisconnectReconnect()


class SignalSection:
    """Minimal section object using real AEtest result signals."""

    uid = 'ResetConfiguration'

    def __init__(self):
        self.parent = Mock()
        self.parent.history = ['Connect']
        self.parent.parameters = {}
        self.parameters = {}

    def failed(self, *args, **kwargs):
        raise AEtestFailedSignal(*args, **kwargs)

    def passed(self, *args, **kwargs):
        raise AEtestPassedSignal(*args, **kwargs)

    def passx(self, *args, **kwargs):
        raise AEtestPassxSignal(*args, **kwargs)


class SignalProcessor:
    """Minimal processor object using real AEtest processor result signals."""

    result_rollup = True

    def failed(self, *args, **kwargs):
        raise ProcessorFailedSignal(*args, **kwargs)

    def errored(self, *args, **kwargs):
        raise ProcessorErroredSignal(*args, **kwargs)

    def passed(self, *args, **kwargs):
        raise ProcessorPassedSignal(*args, **kwargs)

    def passx(self, *args, **kwargs):
        raise ProcessorPassxSignal(*args, **kwargs)


class TestRecovery(unittest.TestCase):

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_aetest_step_reporting(self, recovery_steps):
        class ApplyConfiguration(AEtestTestItem):
            pass

        recovery = partial(
            recovery_processor, configure_console_speed=False)
        recovery.__report__ = True
        processors.affix(ApplyConfiguration, post=[recovery])

        clean = AEtestTestItem(uid='Clean')
        clean.history = {'Connect': object()}
        clean.reporter = Mock()
        device = MagicMock()
        device.chassis_type = 'single'
        device.is_ha = False
        device.state_machine.go_to.side_effect = RuntimeError(
            'reachability failed')
        section = ApplyConfiguration(
            uid='ApplyConfiguration',
            parent=clean,
            parameters={'device': device})
        handler = ProcessorHandler(section)
        processor = handler.post_processors[0]

        handler.stop()

        recovery_steps.assert_called_once()
        self.assertEqual(Passed, section.result)
        self.assertEqual(Passed, clean.result)
        self.assertEqual(Passed, processor.result)
        self.assertFalse(processor.result_rollup)
        self.assertIs(processor, processor.steps.parent)
        self.assertEqual(
            ['Check device reachability', 'Recover the device'],
            [step.name for step in processor.steps.details])
        self.assertEqual(
            [Errored, Passed],
            [step.result for step in processor.steps.details])
        for step in processor.steps.steps:
            self.assertIs(processor.steps, step.parent)

    def test_recovery_processor_device_in_rommon(self):

        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.is_ha = False
        device.state_machine.go_to = MagicMock()
        device.state_machine.current_state = 'rommon'
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.log = logger
        steps = Steps()

        processor = Mock()
        recovery_processor(
            section,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1,
            post_recovery_configuration='hostname recovered',
            configure_console_speed=False,
            processor=processor,
            steps=steps)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()
        device.configure.assert_not_called()
        processor.passed.assert_called_once_with(
            reason='Successfully booted the device.')
        self.assertNotIn('clean_block', section.parent.parameters)
        self.assertNotIn('recovery_outcomes', section.parent.parameters)
        self.assertEqual(
            [Failed, Passed],
            [step.result for step in steps.details])

    def test_recovery_processor_keeps_existing_positional_arguments(self):
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.is_ha = False
        device.state_machine.go_to = MagicMock()
        device.state_machine.current_state = 'rommon'
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.log = logger

        recovery_processor(
            section,
            'Initializing Hardware',
            '\x03',
            True,
            None,
            'c',
            1,
            None,
            ['bootflash:asr1000_golden.bin'],
            None,
            None,
            True,
            True,
            30,
            1,
            None,
            45,
            False,
            processor=Mock())

        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()

    def test_recovery_processor_device_in_rommon_ha(self):
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.is_ha = True
        sub_con_1 = sub_con_2 = MagicMock()
        sub_con_1.state_machine.current_state = sub_con_2.state_machine.current_state = 'rommon'
        device.subconnections = [sub_con_1, sub_con_2]
        device.api.device_boot_recovery = Mock()
        device.api.execute_power_cycle_device = Mock()
        recovery_processor(
            section,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1,
            configure_console_speed=False,
            processor=Mock())
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()

    def test_recovery_processor_device_in_quad(self):
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = "quad"
        device.is_ha = True
        sub_con_1 = sub_con_2 = sub_con_3 = sub_con_4 = MagicMock()
        sub_con_1.state_machine.current_state = sub_con_4.state_machine.current_state = 'rommon'
        device.subconnections = [sub_con_1, sub_con_2, sub_con_3, sub_con_4]
        device.api.device_boot_recovery = Mock()
        device.api.execute_power_cycle_device = Mock()

        recovery_processor(
            section,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1,
            configure_console_speed=False,
            processor=Mock())
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()

    def test_recovery_processor_no_recovery_no_outcome(self):
        section = Mock()
        section.uid = 'VerifyRunningImage'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'single'
        device.is_ha = False
        device.state_machine.current_state = 'enable'
        device.log = logger
        processor = Mock()
        steps = Steps()

        recovery_processor(
            section,
            processor=processor,
            steps=steps,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1,
            configure_console_speed=False)

        self.assertNotIn('clean_block', section.parent.parameters)
        self.assertNotIn('recovery_outcomes', section.parent.parameters)
        self.assertFalse(processor.result_rollup)
        processor.failed.assert_not_called()
        processor.passed.assert_not_called()
        processor.passx.assert_not_called()
        self.assertEqual(
            [Passed, Skipped],
            [step.result for step in steps.details])

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_reconnect_success(
            self, mock_reconnect, recovery_steps):
        mock_reconnect.return_value = True
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'single'
        device.is_ha = False
        device.state_machine.current_state = 'disable'
        device.log = logger
        processor = Mock()
        steps = Steps()

        recovery_processor(
            section,
            processor=processor,
            steps=steps,
            reconnect_delay=1,
            configure_console_speed=False)

        mock_reconnect.assert_called_once_with(device)
        recovery_steps.assert_not_called()
        self.assertNotIn('clean_block', section.parent.parameters)
        self.assertNotIn('recovery_outcomes', section.parent.parameters)
        self.assertEqual(
            [Passed, Skipped],
            [step.result for step in steps.details])

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_reconnect_success_ha(
            self, mock_reconnect, recovery_steps):
        mock_reconnect.return_value = True
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'dual'
        device.is_ha = True
        sub_con_1 = MagicMock()
        sub_con_2 = MagicMock()
        sub_con_1.state_machine.current_state = 'disable'
        sub_con_2.state_machine.current_state = 'disable'
        device.subconnections = [sub_con_1, sub_con_2]
        device.log = logger
        processor = Mock()
        steps = Steps()

        recovery_processor(
            section,
            processor=processor,
            steps=steps,
            reconnect_delay=1,
            configure_console_speed=False)

        mock_reconnect.assert_called_once_with(device)
        recovery_steps.assert_not_called()
        self.assertNotIn('clean_block', section.parent.parameters)
        self.assertNotIn('recovery_outcomes', section.parent.parameters)
        self.assertEqual(
            [Passed, Skipped],
            [step.result for step in steps.details])

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_connect_recovery_success_requests_full_clean_retry(
            self, mock_reconnect):
        mock_reconnect.side_effect = [False, True]
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.api.device_recovery_boot = Mock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.is_ha = False
        device.log = logger
        processor = Mock()
        steps = Steps()

        recovery_processor(
            section,
            processor=processor,
            steps=steps,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1,
            configure_console_speed=False)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_clear_console.assert_called_once()
        device.api.execute_power_cycle_device.assert_called_once()
        block = section.parent.parameters['clean_block']
        self.assertTrue(block['active'])
        self.assertEqual(Blocked, block['result'])
        self.assertFalse(processor.result_rollup)
        processor.passed.assert_called_once()
        outcome = section.parent.parameters['recovery_outcomes']['Connect']
        self.assertEqual(Passed, outcome.result)
        self.assertTrue(outcome.retry_clean)
        self.assertTrue(outcome.terminate_clean)
        self.assertTrue(outcome.block_following_sections)
        self.assertEqual(Blocked, outcome.clean_flow_result)
        self.assertEqual(
            [Errored, Passed],
            [step.result for step in steps.details])
        section.failed.assert_not_called()
        section.passx.assert_not_called()

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_success_raises_processor_passed_signal(
            self, mock_reconnect):
        mock_reconnect.side_effect = [False, True]
        section = SignalSection()
        section.uid = 'Connect'
        processor = SignalProcessor()
        device = section.parameters['device'] = MagicMock()
        device.api.device_recovery_boot = Mock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.is_ha = False
        device.log = logger

        with self.assertRaises(ProcessorPassedSignal) as cm:
            recovery_processor(
                section,
                processor=processor,
                console_activity_pattern='Initializing Hardware',
                console_breakboot_telnet_break=True,
                break_count=1,
                golden_image=['bootflash:asr1000_golden.bin'],
                reconnect_delay=1,
                configure_console_speed=False)

        block = section.parent.parameters['clean_block']
        self.assertTrue(block['active'])
        self.assertEqual(Blocked, block['result'])
        self.assertFalse(processor.result_rollup)
        outcome = section.parent.parameters['recovery_outcomes']['Connect']
        self.assertEqual(Passed, outcome.result)
        self.assertTrue(outcome.retry_clean)
        self.assertTrue(outcome.terminate_clean)
        self.assertTrue(cm.exception.result.reason.startswith(
            "Device '{}' has been recovered - Requesting a full Clean retry"
            .format(device.name)))

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_requires_processor_for_reporting(
            self, mock_reconnect):
        mock_reconnect.side_effect = [False, True]
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.api.device_recovery_boot = Mock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.is_ha = False
        device.log = logger

        with self.assertRaisesRegex(
                RuntimeError,
                "Device recovery result reporting requires an AEtest processor"):
            recovery_processor(
                section,
                console_activity_pattern='Initializing Hardware',
                console_breakboot_telnet_break=True,
                break_count=1,
                golden_image=['bootflash:asr1000_golden.bin'],
                reconnect_delay=1,
                configure_console_speed=False)

        self.assertNotIn('clean_block', section.parent.parameters)
        self.assertNotIn('recovery_outcomes', section.parent.parameters)
        section.passx.assert_not_called()

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_non_connect_success_passed_blocks(self,
                                                                  mock_reconnect):
        mock_reconnect.side_effect = [False, True]
        section = Mock()
        section.uid = 'ResetConfiguration'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.api.device_recovery_boot = Mock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.is_ha = False
        device.log = logger
        processor = SignalProcessor()
        section.result = Passed
        steps = Steps()

        with self.assertRaises(ProcessorPassedSignal) as cm:
            recovery_processor(
                section,
                processor=processor,
                steps=steps,
                console_activity_pattern='Initializing Hardware',
                console_breakboot_telnet_break=True,
                break_count=1,
                golden_image=['bootflash:asr1000_golden.bin'],
                reconnect_delay=1,
                configure_console_speed=False)

        block = section.parent.parameters['clean_block']
        self.assertTrue(block['active'])
        self.assertEqual(Blocked, block['result'])
        self.assertFalse(processor.result_rollup)
        outcome = section.parent.parameters[
            'recovery_outcomes']['ResetConfiguration']
        self.assertEqual(Passed, outcome.result)
        self.assertTrue(outcome.retry_clean)
        self.assertTrue(outcome.terminate_clean)
        self.assertTrue(outcome.block_following_sections)
        self.assertEqual(Blocked, outcome.clean_flow_result)
        self.assertTrue(cm.exception.result.reason.startswith(
            "Device '{d}' has been recovered - Requesting a full "
            "Clean retry".format(d=device.name)))
        self.assertEqual(Passed, section.result)
        self.assertEqual(
            [Errored, Passed],
            [step.result for step in steps.details])
        section.passed.assert_not_called()
        section.failed.assert_not_called()
        section.passx.assert_not_called()

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_non_connect_recovery_failed_blocks(self,
                                                                   mock_reconnect):
        mock_reconnect.side_effect = [False, False]
        section = Mock()
        section.uid = 'ResetConfiguration'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.api.device_recovery_boot = Mock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.is_ha = False
        device.log = logger
        processor = SignalProcessor()
        section.result = Passed
        steps = Steps()

        with self.assertRaises(ProcessorErroredSignal) as cm:
            recovery_processor(
                section,
                processor=processor,
                steps=steps,
                console_activity_pattern='Initializing Hardware',
                console_breakboot_telnet_break=True,
                break_count=1,
                golden_image=['bootflash:asr1000_golden.bin'],
                reconnect_delay=1,
                configure_console_speed=False)

        block = section.parent.parameters['clean_block']
        self.assertTrue(block['active'])
        self.assertEqual(Blocked, block['result'])
        self.assertFalse(processor.result_rollup)
        outcome = section.parent.parameters[
            'recovery_outcomes']['ResetConfiguration']
        self.assertEqual(Errored, outcome.result)
        self.assertFalse(outcome.retry_clean)
        self.assertTrue(outcome.terminate_clean)
        self.assertTrue(outcome.block_following_sections)
        self.assertEqual(Errored, outcome.clean_flow_result)
        self.assertIn(
            "Recovery has failed to restore the device - Blocking clean",
            cm.exception.result.reason)
        self.assertEqual(Passed, section.result)
        self.assertEqual(
            [Errored, Failed],
            [step.result for step in steps.details])
        section.failed.assert_not_called()
        section.passx.assert_not_called()

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_uses_recovery_exception(
            self, recovery_steps):
        reachability_exception = RuntimeError('reachability failed')
        recovery_exception = RuntimeError('recovery failed')
        recovery_steps.side_effect = recovery_exception
        section = SignalSection()
        section.uid = 'ResetConfiguration'
        section.result = Passed
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'single'
        device.is_ha = False
        device.state_machine.go_to.side_effect = reachability_exception
        processor = SignalProcessor()
        steps = Steps()

        with self.assertRaises(ProcessorErroredSignal) as cm:
            recovery_processor(
                section,
                processor=processor,
                steps=steps,
                configure_console_speed=False)

        outcome = section.parent.parameters[
            'recovery_outcomes']['ResetConfiguration']
        self.assertEqual(
            [Errored, Failed],
            [step.result for step in steps.details])
        self.assertIs(recovery_exception, outcome.from_exception)
        self.assertEqual(
            str(recovery_exception), cm.exception.from_exception)
        self.assertNotEqual(
            str(reachability_exception), cm.exception.from_exception)

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_rommon_boot_failure_uses_recovery_steps(
            self, recovery_steps):
        section = Mock()
        section.uid = 'Connect'
        section.result = Passed
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'single'
        device.is_ha = False
        device.state_machine.current_state = 'rommon'
        device.api.device_recovery_boot.side_effect = RuntimeError(
            'direct boot failed')
        steps = Steps()

        recovery_processor(
            section,
            processor=Mock(),
            steps=steps,
            configure_console_speed=False)

        recovery_steps.assert_called_once()
        self.assertEqual(
            [Failed, Passed],
            [step.result for step in steps.details])
        self.assertEqual(Passed, section.result)
        outcome = section.parent.parameters['recovery_outcomes']['Connect']
        self.assertTrue(outcome.retry_clean)
        self.assertTrue(outcome.terminate_clean)

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_post_recovery_configuration_failure(
            self, recovery_steps):
        section = Mock()
        section.uid = 'ResetConfiguration'
        section.result = Passed
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'single'
        device.is_ha = False
        device.state_machine.current_state = 'rommon'
        device.api.device_recovery_boot.side_effect = RuntimeError(
            'direct boot failed')
        device.configure.side_effect = RuntimeError(
            'post recovery configuration failed')
        steps = Steps()

        recovery_processor(
            section,
            processor=Mock(),
            steps=steps,
            post_recovery_configuration='hostname recovered',
            configure_console_speed=False)

        recovery_steps.assert_called_once()
        self.assertEqual(
            [Failed, Failed],
            [step.result for step in steps.details])
        outcome = section.parent.parameters[
            'recovery_outcomes']['ResetConfiguration']
        self.assertTrue(outcome.terminate_clean)
        self.assertEqual(Passed, section.result)

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_recovery_failed_ha(self, mock_reconnect):
        mock_reconnect.side_effect = [False, False]
        section = Mock()
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.api.device_recovery_boot = Mock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.log = logger
        device.is_ha = True
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        sub_con_1 = sub_con_2 = MagicMock()
        sub_con_1.state_machine.go_to = Mock(side_effect=Exception)
        device.subconnections = [sub_con_1, sub_con_2]
        processor = SignalProcessor()
        with self.assertRaises(ProcessorErroredSignal):
            recovery_processor(
                section,
                processor=processor,
                console_activity_pattern='Initializing Hardware',
                console_breakboot_telnet_break=True,
                break_count=1,
                golden_image=['bootflash:asr1000_golden.bin'],
                reconnect_delay=1,
                configure_console_speed=False)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_clear_console.assert_called_once()
        device.api.execute_power_cycle_device.assert_called_once()
        self.assertTrue(section.parent.parameters['clean_block']['active'])
        self.assertFalse(processor.result_rollup)
        section.failed.assert_not_called()
        section.passx.assert_not_called()
        

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect', new=mock_disconnect_reconnect)
    def test_recovery_processor_recovery_configure_console_speed(self):
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.name = 'test_device'
        device.api.device_recovery_boot = Mock(side_effect=[Exception("Boot recovery failed"), None])
        device.api.configure_management_console = Mock()
        device.api.verify_no_boot_manual = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.log = logger
        device.is_ha = True
        device.api.execute_clear_console = Mock()
        sub_con_1 = sub_con_2 = MagicMock()
        sub_con_1.state_machine.go_to = Mock(side_effect=Exception)
        device.subconnections = [sub_con_1, sub_con_2]
        processor = Mock()
        recovery_processor(
            section,
            processor=processor,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1,
            configure_console_speed=True)
        assert device.api.device_recovery_boot.call_count == 2
        assert device.api.execute_power_cycle_device.call_count == 2
        device.api.execute_clear_console.assert_called_once()
        device.api.configure_management_console.assert_called_once()
        device.api.verify_no_boot_manual.assert_called_once()
        self.assertFalse(processor.result_rollup)
        processor.passed.assert_called_once()
        outcome = section.parent.parameters['recovery_outcomes']['Connect']
        self.assertTrue(outcome.retry_clean)
        self.assertTrue(outcome.terminate_clean)
