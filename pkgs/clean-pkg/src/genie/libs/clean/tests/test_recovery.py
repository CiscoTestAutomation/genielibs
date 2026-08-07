import unittest
from unittest.mock import Mock, MagicMock, patch

from unicon import Connection
from unicon.settings import Settings

from pyats.aetest.signals import (
    AEtestFailedSignal,
    AEtestPassedSignal,
    AEtestPassxSignal,
)
from pyats.aetest.processors.signals import (
    ProcessorFailedSignal,
    ProcessorPassedSignal,
    ProcessorPassxSignal,
)
from pyats.results import Blocked, Failed, Passed, Passx

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

    def passed(self, *args, **kwargs):
        raise ProcessorPassedSignal(*args, **kwargs)

    def passx(self, *args, **kwargs):
        raise ProcessorPassxSignal(*args, **kwargs)


class TestRecovery(unittest.TestCase):

    def test_recovery_processor_device_in_rommon(self):

        section = Mock()
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
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1,
            configure_console_speed=False)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()

    def test_recovery_processor_keeps_existing_positional_arguments(self):
        section = Mock()
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
            False)

        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()

    def test_recovery_processor_device_in_rommon_ha(self):
        section = Mock()
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
            configure_console_speed=False)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()

    def test_recovery_processor_device_in_quad(self):
        section = Mock()
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
            configure_console_speed=False)
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

        recovery_processor(
            section,
            processor=processor,
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

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_recovery_success_passx(self, mock_reconnect):
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
        self.assertNotIn('clean_block', section.parent.parameters)
        self.assertFalse(processor.result_rollup)
        processor.passx.assert_called_once_with(
            reason="Device has been recovered. Continuing with pyATS Clean.")
        outcome = section.parent.parameters['recovery_outcomes']['Connect']
        self.assertEqual(Passx, outcome.result)
        self.assertTrue(outcome.continue_clean)
        self.assertFalse(outcome.terminate_clean)
        self.assertEqual(Passx, section.result)
        section.failed.assert_not_called()
        section.passx.assert_not_called()

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_success_raises_processor_passx_signal(
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

        with self.assertRaises(ProcessorPassxSignal) as cm:
            recovery_processor(
                section,
                processor=processor,
                console_activity_pattern='Initializing Hardware',
                console_breakboot_telnet_break=True,
                break_count=1,
                golden_image=['bootflash:asr1000_golden.bin'],
                reconnect_delay=1,
                configure_console_speed=False)

        self.assertNotIn('clean_block', section.parent.parameters)
        self.assertFalse(processor.result_rollup)
        self.assertEqual(Passx, section.result)
        self.assertEqual(
            cm.exception.result.reason,
            "Device has been recovered. Continuing with pyATS Clean.")

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
        outcome = section.parent.parameters[
            'recovery_outcomes']['ResetConfiguration']
        self.assertEqual(Passed, outcome.result)
        self.assertTrue(outcome.terminate_clean)
        self.assertTrue(outcome.block_following_sections)
        self.assertEqual(Blocked, outcome.clean_flow_result)
        self.assertEqual(
            cm.exception.result.reason,
            "Device '{d}' has been recovered - "
            "Terminating clean".format(d=device.name))
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

        with self.assertRaises(ProcessorFailedSignal) as cm:
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
        outcome = section.parent.parameters[
            'recovery_outcomes']['ResetConfiguration']
        self.assertEqual(Failed, outcome.result)
        self.assertTrue(outcome.terminate_clean)
        self.assertTrue(outcome.block_following_sections)
        self.assertEqual(Failed, outcome.clean_flow_result)
        self.assertIn(
            "Recovery has failed to restore the device - Blocking clean",
            cm.exception.result.reason)
        self.assertIn("Cannot recover the device", cm.exception.result.reason)
        section.failed.assert_not_called()
        section.passx.assert_not_called()

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
        with self.assertRaises(ProcessorFailedSignal):
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
        processor.passx.assert_called_once_with(
            reason="Device has been recovered. Continuing with pyATS Clean.")
