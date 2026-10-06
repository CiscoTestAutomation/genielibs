import unittest
from functools import partial
from unittest.mock import Mock, MagicMock, call, patch

from unicon import Connection
from unicon.core.errors import EOF
from unicon.eal.backend.pty_backend import Spawn as PtySpawn
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

from genie.libs.clean.recovery.recovery import (
    _process_recovery_outcome,
    _recovery_steps,
    bring_to_any_state,
    recovery_processor,
)

import logging

logger = logging.getLogger(__name__)


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

    @patch(
        'genie.libs.clean.recovery.recovery._disconnect_reconnect',
        return_value=True)
    def test_recovery_steps_accepts_legacy_clear_line_none_as_success(
            self, mock_reconnect):
        device = MagicMock(name='device')
        device.name = 'device'
        device.api.execute_clear_line = Mock(return_value=None)

        _recovery_steps(device)

        device.api.execute_clear_line.assert_called_once_with()
        device.api.execute_clear_console.assert_not_called()
        mock_reconnect.assert_called_once_with(device)
        device.api.execute_power_cycle_device.assert_not_called()
        device.api.device_recovery_boot.assert_not_called()

    @patch('genie.libs.clean.recovery.recovery.time.sleep')
    @patch(
        'genie.libs.clean.recovery.recovery._disconnect_reconnect',
        return_value=True)
    def test_recovery_steps_does_not_treat_failed_clear_line_as_success(
            self, mock_reconnect, _sleep):
        device = MagicMock(name='device')
        device.name = 'device'
        device.api.execute_clear_line.return_value = False

        _recovery_steps(
            device, powercycler=False, reconnect_delay=0)

        device.api.execute_clear_line.assert_called_once_with()
        device.api.device_recovery_boot.assert_called_once_with()
        mock_reconnect.assert_called_once_with(device)

    def test_failed_recovery_merges_with_existing_stage_result(self):
        for stage_result, expected_result in (
                (Passed, Failed),
                (Failed, Failed),
                (Errored, Errored)):
            with self.subTest(stage_result=stage_result):
                section = SignalSection()
                section.result = stage_result
                processor = SignalProcessor()

                with self.assertRaises(ProcessorFailedSignal):
                    _process_recovery_outcome(
                        section,
                        processor=processor,
                        processor_result=Failed,
                        section_result=Failed,
                        reason='Device recovery failed')

                self.assertEqual(expected_result, section.result)
                self.assertFalse(processor.result_rollup)

    def test_bring_to_any_state_preserves_spawn_eof(self):
        connection_failure = EOF('original connection failure')
        connection = Mock()
        connection.spawn.sendline.side_effect = connection_failure

        with self.assertRaises(EOF) as cm:
            bring_to_any_state(connection, 45)

        self.assertIs(connection_failure, cm.exception)
        connection.spawn.sendline.assert_called_once_with()
        connection.state_machine.go_to.assert_not_called()

    def test_bring_to_any_state_rejects_missing_spawn(self):
        connection = Mock()
        connection.spawn = None

        with self.assertRaisesRegex(EOF, 'spawn is closed'):
            bring_to_any_state(connection, 45)

        connection.state_machine.go_to.assert_not_called()

    def test_bring_to_any_state_rejects_actual_closed_spawn(self):
        settings = Settings()
        settings.POST_DISCONNECT_WAIT_SEC = 0
        settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0
        spawn = PtySpawn('sh', settings=settings)
        spawn.close()
        connection = Mock(spawn=spawn)

        with patch.object(
                spawn, 'sendline', wraps=spawn.sendline) as sendline, \
                self.assertRaisesRegex(EOF, 'spawn is closed'):
            bring_to_any_state(connection, 45)

        sendline.assert_not_called()
        connection.state_machine.go_to.assert_not_called()

    def test_bring_to_any_state_uses_spawn_is_closed_api(self):
        class Spawn:

            fd = None

            def __init__(self, closed):
                self.closed = closed
                self.is_closed_calls = 0
                self.sendline = Mock()

            def is_closed(self):
                self.is_closed_calls += 1
                return self.closed

        closed_spawn = Spawn(True)
        closed_connection = Mock(spawn=closed_spawn)
        with self.assertRaisesRegex(EOF, 'spawn is closed'):
            bring_to_any_state(closed_connection, 45)
        self.assertEqual(1, closed_spawn.is_closed_calls)
        closed_spawn.sendline.assert_not_called()
        closed_connection.state_machine.go_to.assert_not_called()

        live_spawn = Spawn(False)
        live_connection = Mock(spawn=live_spawn)
        live_connection.context = {}
        bring_to_any_state(live_connection, 45)
        self.assertEqual(1, live_spawn.is_closed_calls)
        live_spawn.sendline.assert_called_once_with()
        live_connection.state_machine.go_to.assert_called_once_with(
            'any', live_spawn, timeout=45, context=live_connection.context)

    def test_bring_to_any_state_preserves_state_failure(self):
        state_failure = RuntimeError('state transition failed')
        connection = Mock()
        connection.context = {}
        connection.state_machine.go_to.side_effect = state_failure

        with self.assertRaises(RuntimeError) as cm:
            bring_to_any_state(connection, 45)

        self.assertIs(state_failure, cm.exception)
        connection.spawn.sendline.assert_called_once_with()

    def test_bring_to_any_state_uses_stable_spawn_reference(self):
        class CustomSpawn:

            def __init__(self):
                self.sendline = Mock()

        connection = Mock(spawn=CustomSpawn())
        connection.context = {}
        original_spawn = connection.spawn
        replacement_spawn = object()
        original_spawn.sendline.side_effect = lambda: setattr(
            connection, 'spawn', replacement_spawn)

        bring_to_any_state(connection, 45)

        original_spawn.sendline.assert_called_once_with()
        self.assertIs(replacement_spawn, connection.spawn)
        connection.state_machine.go_to.assert_called_once_with(
            'any', original_spawn, timeout=45,
            context=connection.context)

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_preserves_spawn_eof(
            self, recovery_steps):
        connection_failure = EOF('original connection failure')
        section = Mock()
        section.uid = 'ResetConfiguration'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'single'
        device.is_ha = False
        device.spawn.sendline.side_effect = connection_failure
        device.state_machine.current_state = 'enable'
        processor = Mock()
        steps = Steps()

        recovery_processor(
            section,
            processor=processor,
            steps=steps,
            configure_console_speed=False)

        device.spawn.sendline.assert_called_once_with()
        recovery_steps.assert_called_once_with(
            device, True, True, 30, 60, False)
        self.assertEqual(
            [Errored, Passed],
            [step.result for step in steps.details])
        self.assertIn(
            str(connection_failure), steps.details[0].result.reason)

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

    @patch(
        'genie.libs.clean.recovery.iosxe.recovery.device_recovery')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_mixed_ha_states_with_rommon(
            self, recovery_steps, disconnect_reconnect, device_recovery):
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'stack'
        device.is_ha = True
        device.os = 'iosxe'
        active = MagicMock()
        rommon = MagicMock()
        standby = MagicMock()
        active.state_machine.current_state = 'enable'
        rommon.state_machine.current_state = 'rommon'
        standby.state_machine.current_state = 'enable'
        device.subconnections = [active, rommon, standby]
        device.api.device_recovery_boot = Mock()
        device.api.execute_power_cycle_device = Mock()
        disconnect_reconnect.return_value = True

        recovery_processor(
            section,
            golden_image=['flash:cat9k.bin'],
            reconnect_delay=1,
            configure_console_speed=False,
            processor=Mock())

        device.api.device_recovery_boot.assert_not_called()
        device_recovery.assert_called_once_with(
            rommon, 750, ['flash:cat9k.bin'], None)
        disconnect_reconnect.assert_called_once_with(
            device, connection_timeout=750)
        device.api.execute_power_cycle_device.assert_not_called()
        recovery_steps.assert_not_called()

    @patch(
        'genie.libs.clean.recovery.iosxe.recovery.device_recovery')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_mixed_ha_states_with_dict_golden_image(
            self, recovery_steps, disconnect_reconnect, device_recovery):
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'stack'
        device.is_ha = True
        device.os = 'iosxe'
        active = MagicMock()
        rommon = MagicMock()
        active.state_machine.current_state = 'enable'
        rommon.state_machine.current_state = 'rommon'
        device.subconnections = [active, rommon]
        disconnect_reconnect.return_value = True

        recovery_processor(
            section,
            golden_image={'system': 'flash:cat9k.bin'},
            reconnect_delay=1,
            configure_console_speed=False,
            processor=Mock())

        device_recovery.assert_called_once_with(
            rommon, 750, ['flash:cat9k.bin'], None)
        disconnect_reconnect.assert_called_once_with(
            device, connection_timeout=750)
        recovery_steps.assert_not_called()

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_initializes_successful_mit_reconnect(
            self, recovery_steps, disconnect_reconnect):
        section = Mock()
        section.uid = 'ApplyConfiguration'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'stack'
        device.is_ha = True
        device.os = 'iosxe'
        active = MagicMock()
        standby = MagicMock()
        active.state_machine.current_state = 'enable'
        standby.state_machine.current_state = 'enable'
        active.state_machine.go_to.side_effect = RuntimeError(
            'Failed while bringing device to any state')
        device.subconnections = [active, standby]
        disconnect_reconnect.return_value = True

        recovery_processor(
            section,
            golden_image=['flash:cat9k.bin'],
            reconnect_delay=1,
            configure_console_speed=False,
            processor=Mock(),
            steps=Steps())

        disconnect_reconnect.assert_called_once_with(
            device, connection_timeout=45, mit=True)
        self.assertFalse(device.default.mit)
        self.assertFalse(device.default.learn_hostname)
        device.connection_provider.init_connection.assert_called_once_with()
        recovery_steps.assert_not_called()

    @patch(
        'genie.libs.clean.recovery.iosxe.recovery.device_recovery')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_other_mixed_ha_devices_use_recovery_steps(
            self, recovery_steps, disconnect_reconnect, device_recovery):
        for device_os, chassis_type in (
                ('nxos', 'stack'),
                ('iosxe', 'dual_rp')):
            with self.subTest(
                    device_os=device_os, chassis_type=chassis_type):
                recovery_steps.reset_mock()
                disconnect_reconnect.reset_mock()
                device_recovery.reset_mock()
                section = Mock()
                section.uid = 'Connect'
                section.parent = Mock()
                section.parent.history = ['Connect']
                section.parent.parameters = {}
                section.parameters = {}
                device = section.parameters['device'] = MagicMock()
                device.chassis_type = chassis_type
                device.is_ha = True
                device.os = device_os
                active = MagicMock()
                rommon = MagicMock()
                active.state_machine.current_state = 'enable'
                rommon.state_machine.current_state = 'rommon'
                device.subconnections = [active, rommon]
                device.api.device_recovery_boot = Mock()

                recovery_processor(
                    section,
                    golden_image=[f'bootflash:{device_os}.bin'],
                    reconnect_delay=1,
                    configure_console_speed=False,
                    processor=Mock())

                device.api.device_recovery_boot.assert_not_called()
                device_recovery.assert_not_called()
                disconnect_reconnect.assert_not_called()
                recovery_steps.assert_called_once_with(
                    device, True, True, 30, 1, False)

    @patch(
        'genie.libs.clean.recovery.iosxe.recovery.device_recovery')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    def test_recovery_processor_ha_state_check_failure_attempts_boot_recovery(
            self, recovery_steps, disconnect_reconnect, device_recovery):
        section = Mock()
        section.uid = 'ApplyConfiguration'
        section.result = Failed
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'stack'
        device.is_ha = True
        device.os = 'iosxe'
        active = MagicMock()
        booting = MagicMock()
        standby = MagicMock()
        active.state_machine.current_state = 'enable'
        booting.state_machine.current_state = 'enable'
        standby.state_machine.current_state = 'enable'

        def update_booting_state(*args, **kwargs):
            raise RuntimeError(
                'Failed while bringing device to any state')

        def reconnect_with_rommon_state(*args, **kwargs):
            if kwargs.get('mit'):
                booting.state_machine.current_state = 'rommon'
            return True

        booting.state_machine.go_to.side_effect = update_booting_state
        device.subconnections = [active, booting, standby]
        device.api.device_recovery_boot = Mock()
        device.api.execute_power_cycle_device = Mock()
        tftp_boot = {
            'image': ['cat9k.bin'],
            'ip_address': ['192.0.2.1'],
            'subnet_mask': '255.255.255.0',
            'gateway': '192.0.2.254',
            'tftp_server': '192.0.2.2',
        }
        device.clean = {'device_recovery': {'tftp_boot': tftp_boot}}
        device.api.get_recovery_details.return_value = {
            'tftp_boot': tftp_boot,
        }
        device.api.get_tftp_boot_command.return_value = (
            'tftp:', 'cat9k.bin')
        disconnect_reconnect.side_effect = reconnect_with_rommon_state
        processor = Mock()
        steps = Steps()

        recovery_processor(
            section,
            tftp_boot=tftp_boot,
            reconnect_delay=1,
            configure_console_speed=False,
            processor=processor,
            steps=steps)

        device.api.device_recovery_boot.assert_not_called()
        device.api.get_recovery_details.assert_called_once_with(
            tftp_boot=tftp_boot)
        device.api.get_tftp_boot_command.assert_called_once_with(
            {'tftp_boot': tftp_boot})
        device.api.configure_rommon_tftp_ha.assert_called_once_with(
            image_path='cat9k.bin')
        device_recovery.assert_called_once_with(
            booting, 750, ['tftp:'], None)
        device.api.execute_power_cycle_device.assert_not_called()
        disconnect_reconnect.assert_has_calls([
            call(device, connection_timeout=45, mit=True),
            call(device, connection_timeout=750),
        ])
        self.assertEqual(2, disconnect_reconnect.call_count)
        recovery_steps.assert_not_called()
        processor.passed.assert_called_once_with(
            reason='Successfully booted the device.')
        self.assertFalse(processor.result_rollup)
        self.assertEqual(Failed, section.result)
        self.assertEqual(
            [Errored, Passed],
            [step.result for step in steps.details])
        self.assertNotIn('clean_block', section.parent.parameters)
        self.assertNotIn('recovery_outcomes', section.parent.parameters)

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

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_ha_enable_disable_states_are_reachable(
            self, mock_reconnect, recovery_steps):
        for states in (
                ('enable', 'enable', 'enable'),
                ('enable', 'enable', 'disable'),
                ('enable', 'disable', 'disable'),
                ('disable', 'enable', 'disable'),
                ('disable', 'disable', 'enable')):
            with self.subTest(states=states):
                mock_reconnect.reset_mock()
                recovery_steps.reset_mock()
                section = Mock()
                section.uid = 'Connect'
                section.parent = Mock()
                section.parent.history = ['Connect']
                section.parent.parameters = {}
                section.parameters = {}
                device = section.parameters['device'] = MagicMock()
                device.chassis_type = 'stack'
                device.is_ha = True
                device.os = 'iosxe'
                device.subconnections = []
                for state in states:
                    connection = MagicMock()
                    connection.state_machine.current_state = state
                    device.subconnections.append(connection)
                steps = Steps()

                recovery_processor(
                    section,
                    processor=Mock(),
                    steps=steps,
                    reconnect_delay=1,
                    configure_console_speed=False)

                mock_reconnect.assert_not_called()
                recovery_steps.assert_not_called()
                self.assertEqual(
                    [Passed, Skipped],
                    [step.result for step in steps.details])

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_ha_all_disable_reconnects(
            self, mock_reconnect, recovery_steps):
        mock_reconnect.return_value = True
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'stack'
        device.is_ha = True
        device.os = 'iosxe'
        device.subconnections = []
        for state in ('disable', 'disable', 'disable'):
            connection = MagicMock()
            connection.state_machine.current_state = state
            device.subconnections.append(connection)
        steps = Steps()

        recovery_processor(
            section,
            processor=Mock(),
            steps=steps,
            reconnect_delay=1,
            configure_console_speed=False)

        mock_reconnect.assert_called_once_with(device)
        recovery_steps.assert_not_called()
        self.assertEqual(
            [Passed, Skipped],
            [step.result for step in steps.details])

    @patch('genie.libs.clean.recovery.recovery._recovery_steps')
    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_ha_empty_subconnections_reconnects(
            self, mock_reconnect, recovery_steps):
        mock_reconnect.return_value = True
        section = Mock()
        section.uid = 'Connect'
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.chassis_type = 'stack'
        device.is_ha = True
        device.os = 'iosxe'
        device.subconnections = []
        device.api.device_recovery_boot = Mock()
        steps = Steps()

        recovery_processor(
            section,
            processor=Mock(),
            steps=steps,
            reconnect_delay=1,
            configure_console_speed=False)

        mock_reconnect.assert_called_once_with(device)
        device.api.device_recovery_boot.assert_not_called()
        recovery_steps.assert_not_called()
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
        device.api.execute_clear_line = Mock()
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
        device.api.execute_clear_line.assert_called_once()
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
        section.result = Failed
        processor = SignalProcessor()
        device = section.parameters['device'] = MagicMock()
        device.api.device_recovery_boot = Mock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_line = Mock()
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
        self.assertEqual(Failed, section.result)
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
        device.api.execute_clear_line = Mock()
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
        device.api.execute_clear_line = Mock()
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
        device.api.execute_clear_line = Mock()
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
        self.assertEqual(Errored, section.result)
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
        self.assertEqual(Errored, section.result)

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
        self.assertEqual(Failed, section.result)

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_recovery_failed_ha(self, mock_reconnect):
        mock_reconnect.side_effect = [False, False]
        section = Mock()
        section.result = Passed
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.api.device_recovery_boot = Mock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_line = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.log = logger
        device.is_ha = True
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_line = Mock()
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
        device.api.execute_clear_line.assert_called_once()
        device.api.execute_power_cycle_device.assert_called_once()
        self.assertTrue(section.parent.parameters['clean_block']['active'])
        self.assertFalse(processor.result_rollup)
        self.assertEqual(Errored, section.result)
        section.failed.assert_not_called()
        section.passx.assert_not_called()
        

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect')
    def test_recovery_processor_recovery_configure_console_speed(
            self, disconnect_reconnect):
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
        device.api.device_recovery_boot = Mock(
            side_effect=[
                Exception("Boot recovery failed"),
                None,
            ])
        device.api.configure_management_console = Mock()
        device.api.verify_no_boot_manual = Mock()
        device.api.execute_clear_line = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.log = logger
        device.is_ha = True
        device.api.execute_clear_line = Mock()
        sub_con_1 = sub_con_2 = MagicMock()
        sub_con_1.state_machine.go_to = Mock(side_effect=Exception)
        device.subconnections = [sub_con_1, sub_con_2]
        disconnect_reconnect.side_effect = [False, True]
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
        disconnect_reconnect.assert_has_calls([
            call(device),
            call(device),
        ])
        self.assertEqual(2, disconnect_reconnect.call_count)
        assert device.api.device_recovery_boot.call_count == 2
        assert device.api.execute_power_cycle_device.call_count == 2
        device.api.execute_clear_line.assert_called_once()
        device.api.configure_management_console.assert_called_once()
        device.api.verify_no_boot_manual.assert_called_once()
        self.assertFalse(processor.result_rollup)
        processor.passed.assert_called_once()
        outcome = section.parent.parameters['recovery_outcomes']['Connect']
        self.assertTrue(outcome.retry_clean)
        self.assertTrue(outcome.terminate_clean)
