import unittest
import re
import threading
from concurrent.futures import ALL_COMPLETED, Future
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

from unicon import Connection
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement
from unicon.plugins.generic.patterns import GenericPatterns
from unicon.plugins.generic.statements import generic_statements
from unicon.statemachine import State, StateMachine

from genie.libs.sdk.apis.iosxe.rommon.utils import send_break_boot


class TestSendBreakBoot(unittest.TestCase):

    def _setup_sync_executor(self, mock_executor, mock_wait):
        executor = Mock()

        def _submit(fn, *args, **kwargs):
            future = Future()
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                future.set_exception(exc)
            else:
                future.set_result(result)
            return future

        executor.submit.side_effect = _submit
        executor.shutdown.return_value = None
        mock_executor.return_value = executor
        mock_wait.side_effect = lambda futures, timeout, return_when: \
            (set(futures), set())

    def _build_device(self, rommon_prompt='rommon>'):
        class RommonStateMachine(StateMachine):
            def create(self):
                self.add_state(State('generic', 'generic>'))
                self.add_state(State('rommon', rommon_prompt))
                self.add_state(State('enable', 'uut#'))

        device = Mock()
        device.name = 'uut'
        device.is_ha = False
        device.connected = True
        device.credentials = {}
        device.connection_provider.get_connection_dialog.return_value = \
            Dialog()

        conn = Mock()
        conn.context = {}
        conn.connect_reply = Dialog()
        conn.connection_timeout = 30
        conn.mit = False
        conn.connected = True
        conn.state_machine = RommonStateMachine()
        conn.state_machine.go_to = Mock(wraps=conn.state_machine.go_to)
        conn.spawn.timeout = 1
        conn.spawn.log.info = Mock()
        conn.spawn.log.debug = Mock()
        conn.spawn.settings.PROMPT_RECOVERY_COMMANDS = []
        conn.spawn.settings.PROMPT_RECOVERY_INTERVAL = 0
        conn.spawn.settings.PROMPT_RECOVERY_RETRIES = 0
        conn.spawn.read_update_buffer.return_value = True
        conn.spawn.match = SimpleNamespace(
            last_match='rommon>',
            match_output='rommon>',
            last_match_mode=None,
        )
        device.default = conn

        return device, conn

    def _match_state(self, state_name):
        def _match_buffer(patterns):
            for index, pattern in enumerate(patterns):
                if state_name in getattr(pattern, 'pattern', str(pattern)):
                    return index
            return False

        return _match_buffer

    def _match_buffer(self, spawn):
        def match_buffer(patterns):
            for index, pattern in enumerate(patterns):
                pattern = getattr(pattern, 'pattern', pattern)
                last_line = pattern.endswith('$') and \
                    not pattern.endswith(r'\$')
                if last_line:
                    if pattern.endswith(r'\s*$'):
                        lines = spawn.buffer.rstrip().splitlines(
                            keepends=True)
                    else:
                        lines = spawn.buffer.splitlines(keepends=True)
                    match = re.search(pattern, lines[-1], re.S) \
                        if lines else None
                else:
                    match = re.search(pattern, spawn.buffer, re.S)
                if match:
                    spawn.match.last_match = match
                    spawn.match.match_output = \
                        spawn.buffer if last_line else match.group()
                    spawn.match.last_match_mode = last_line
                    return index
            return False

        return match_buffer

    def _trim_buffer(self, spawn):
        def trim_buffer():
            if spawn.match.last_match_mode:
                spawn.buffer = ''
            else:
                spawn.buffer = spawn.buffer[
                    spawn.match.last_match.end():]

        return trim_buffer

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_send_break_boot_updates_current_state_from_dialog_match(
        self, mock_executor, mock_wait
    ):
        """Matched rommon prompt updates current_state without extra probe."""
        device, con = self._build_device()
        con.spawn.match_buffer.side_effect = self._match_state('rommon')
        self._setup_sync_executor(mock_executor, mock_wait)

        send_break_boot(device, timeout=1)

        self.assertEqual(con.state_machine.current_state, 'rommon')
        con.state_machine.go_to.assert_not_called()
        con.sendline.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_send_break_boot_falls_back_to_go_to_any(
        self, mock_executor, mock_wait
    ):
        """Keep old state discovery when rommon prompt was not matched."""
        device, con = self._build_device()
        con.spawn.match_buffer.side_effect = self._match_state('generic')
        con.state_machine.go_to = Mock(
            side_effect=lambda *args, **kwargs:
                con.state_machine.update_cur_state('rommon'))
        self._setup_sync_executor(mock_executor, mock_wait)

        send_break_boot(device, timeout=1)

        con.sendline.assert_called_once()
        con.state_machine.go_to.assert_called_once_with(
            'any', spawn=con.spawn, context=con.context, timeout=1)
        self.assertEqual(con.state_machine.current_state, 'rommon')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.log.info')
    def test_send_break_boot_sends_one_ctrl_c_at_switch_prompt(
        self, mock_log, mock_executor, mock_wait, mock_sleep
    ):
        """Send one break before stopping at an existing switch prompt."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        con.spawn.buffer = '....\r\nswitch:'
        con.spawn.match_buffer.side_effect = self._match_buffer(con.spawn)
        con.spawn.trim_buffer.side_effect = self._trim_buffer(con.spawn)
        self._setup_sync_executor(mock_executor, mock_wait)

        send_break_boot(
            device,
            console_activity_pattern=r'\.\.\.\.',
            console_breakboot_char='\x03',
            break_count=15,
            timeout=1)

        self.assertEqual(con.state_machine.current_state, 'rommon')
        con.state_machine.go_to.assert_not_called()
        mock_log.assert_any_call(
            'Found the console_activity_pattern! Breaking the boot process.')
        con.spawn.send.assert_called_once_with('\x03')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_send_break_boot_stops_after_switch_prompt_arrives(
        self, mock_executor, mock_wait, mock_sleep
    ):
        """Stop the break sequence when switch prompt arrives."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        con.spawn.buffer = '....'
        con.spawn.match_buffer.side_effect = self._match_buffer(con.spawn)
        con.spawn.trim_buffer.side_effect = self._trim_buffer(con.spawn)

        def _read_update_buffer():
            if con.spawn.send.call_count == 1 and \
                    'switch:' not in con.spawn.buffer:
                con.spawn.buffer += '\r\nswitch: '
            return True

        con.spawn.read_update_buffer.side_effect = _read_update_buffer
        self._setup_sync_executor(mock_executor, mock_wait)

        send_break_boot(
            device,
            console_activity_pattern=r'\.\.\.\.',
            console_breakboot_char='\x03',
            break_count=15,
            timeout=1)

        self.assertEqual(con.state_machine.current_state, 'rommon')
        con.state_machine.go_to.assert_not_called()
        con.spawn.send.assert_called_once_with('\x03')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_send_break_boot_sends_all_ctrl_c_without_rommon_prompt(
        self, mock_executor, mock_wait, mock_sleep
    ):
        """Keep the configured break count when no ROMMON prompt appears."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        con.spawn.buffer = '....'
        con.spawn.match_buffer.side_effect = self._match_buffer(con.spawn)
        con.spawn.trim_buffer.side_effect = self._trim_buffer(con.spawn)
        con.state_machine.go_to = Mock(
            side_effect=lambda *args, **kwargs:
                con.state_machine.update_cur_state('rommon'))

        def _read_update_buffer():
            if con.spawn.send.call_count == 3 and not con.spawn.buffer:
                con.spawn.buffer = 'generic>'
            return True

        con.spawn.read_update_buffer.side_effect = _read_update_buffer
        self._setup_sync_executor(mock_executor, mock_wait)

        send_break_boot(
            device,
            console_activity_pattern=r'\.\.\.\.',
            console_breakboot_char='\x03',
            break_count=3,
            timeout=1)

        self.assertEqual(con.spawn.send.call_args_list, [call('\x03')] * 3)

    @patch.object(Dialog, 'process', autospec=True)
    def test_telnet_breakboot_stops_before_send_break_when_cancelled(
            self, mock_process):
        """Cancellation after the Telnet prompt prevents further input."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)

        def _process(dialog, spawn, **kwargs):
            statement = next(
                statement for statement in dialog
                if statement.action.__name__ == 'telnet_breakboot')
            cancel_event = statement.args['cancel_event']

            def _expect(pattern):
                self.assertEqual(pattern, r'telnet>\s*$')
                cancel_event.set()

            spawn.expect.side_effect = _expect
            statement.action(spawn, **statement.args)
            con.state_machine.update_cur_state('rommon')

        mock_process.side_effect = _process

        send_break_boot(
            device,
            console_breakboot_telnet_break=True,
            break_count=2,
            timeout=1)

        con.spawn.send.assert_called_once_with('\x1d')
        con.spawn.sendline.assert_not_called()
        con.spawn.expect.assert_called_once_with(r'telnet>\s*$')

    def test_unconnected_device_uses_normal_unicon_connect(self):
        """Connection recovery stays in Unicon and learns the real state."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        device.connected = False
        con.connected = False
        con.connect_reply = Dialog([
            Statement(pattern='standard connection prompt',
                      action='sendline()')
        ])
        connect_reply = con.connect_reply

        def _connect(connection_dialog, skip_initialization):
            self.assertTrue(skip_initialization)
            self.assertEqual(con.connection_timeout, 1)
            refused_statement = next(iter(connection_dialog))
            self.assertEqual(
                refused_statement.pattern,
                generic_statements.connection_refused_stmt.pattern)
            self.assertEqual(
                refused_statement.action.__name__,
                'connection_refused_handler')
            self.assertIn(r'\.\.\.\.', str(connection_dialog))
            self.assertNotIn('standard connection prompt',
                             str(connection_dialog))
            self.assertIs(con.connect_reply, connect_reply)
            con.state_machine.update_cur_state('rommon')

        con.connect.side_effect = _connect

        result = send_break_boot(device, timeout=1)

        device.setup_connection.assert_not_called()
        con.connect.assert_called_once()
        self.assertIsInstance(
            con.connect.call_args.kwargs['connection_dialog'], Dialog)
        self.assertTrue(
            con.connect.call_args.kwargs['skip_initialization'])
        device.connect.assert_not_called()
        self.assertIsNone(result)
        self.assertEqual(con.state_machine.current_state, 'rommon')
        self.assertFalse(con.mit)
        self.assertIs(con.connect_reply, connect_reply)
        self.assertEqual(con.connection_timeout, 30)

    def test_unconnected_device_rejects_unsupported_unicon(self):
        """Do not silently ignore required connection overrides."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        device.connected = False
        con.connected = False

        def legacy_connect(self, *args, **kwargs):
            pass

        with patch.object(Connection, 'connect', legacy_connect):
            with self.assertRaisesRegex(
                    SubCommandFailure,
                    'supports connection_dialog and skip_initialization'):
                send_break_boot(device, timeout=1)

        con.connect.assert_not_called()

    def test_unconnected_device_preserves_telnet_and_grub_break_modes(self):
        """The public connect path retains every supported break mechanism."""
        cases = (
            (
                {'console_breakboot_telnet_break': True},
                [
                    (generic_statements.connection_refused_stmt.pattern,
                     'connection_refused_handler'),
                    (r'\.\.\.\.', 'telnet_breakboot'),
                ],
            ),
            (
                {
                    'grub_activity_pattern': 'grub activity',
                    'grub_breakboot_char': 'c',
                },
                [
                    (generic_statements.connection_refused_stmt.pattern,
                     'connection_refused_handler'),
                    (r'\.\.\.\.', 'console_breakboot'),
                    ('grub activity', 'grub_breakboot'),
                ],
            ),
        )

        for arguments, expected_statements in cases:
            with self.subTest(arguments=arguments):
                device, con = self._build_device(
                    GenericPatterns().rommon_prompt)
                device.connected = False
                con.connected = False

                def _connect(connection_dialog, skip_initialization):
                    self.assertTrue(skip_initialization)
                    actual_statements = [
                        (statement.pattern, statement.action.__name__)
                        for statement in connection_dialog
                    ]
                    self.assertEqual(
                        actual_statements, expected_statements)
                    con.state_machine.update_cur_state('rommon')

                con.connect.side_effect = _connect

                send_break_boot(device, timeout=1, **arguments)

                con.connect.assert_called_once()
                device.connect.assert_not_called()

    def test_unconnected_device_restores_connection_attributes_on_error(self):
        """The temporary timeout is restored when connect fails."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        device.connected = False
        con.connected = False
        connect_reply = con.connect_reply
        con.connect.side_effect = ConnectionRefusedError('refused')

        with self.assertRaisesRegex(ConnectionRefusedError, 'refused'):
            send_break_boot(device, timeout=1)

        self.assertFalse(con.mit)
        self.assertIs(con.connect_reply, connect_reply)
        self.assertEqual(con.connection_timeout, 30)

    def test_unconnected_device_restores_attributes_on_dialog_error(self):
        """Restore the timeout if the break dialog cannot be built."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        device.connected = False
        con.connected = False
        connect_reply = con.connect_reply
        con.state_machine.get_state = Mock(
            side_effect=RuntimeError('dialog failed'))

        with self.assertRaisesRegex(RuntimeError, 'dialog failed'):
            send_break_boot(device, timeout=1)

        con.connect.assert_not_called()
        device.connect.assert_not_called()
        self.assertFalse(con.mit)
        self.assertIs(con.connect_reply, connect_reply)
        self.assertEqual(con.connection_timeout, 30)

    def test_unconnected_device_restores_redirected_connection(self):
        """Validation follows a replacement without modifying its settings."""
        device, old_con = self._build_device(GenericPatterns().rommon_prompt)
        _, new_con = self._build_device(GenericPatterns().rommon_prompt)
        device.connected = False
        old_con.connected = False
        old_con.state_machine.update_cur_state('enable')
        new_con.mit = True
        new_con.connection_timeout = 1
        new_con.state_machine.update_cur_state('rommon')

        def _connect(connection_dialog, skip_initialization):
            self.assertTrue(skip_initialization)
            device.default = new_con

        old_con.connect.side_effect = _connect

        send_break_boot(device, timeout=1)

        old_con.sendline.assert_not_called()
        new_con.sendline.assert_not_called()
        self.assertFalse(old_con.mit)
        self.assertTrue(new_con.mit)
        self.assertEqual(old_con.connection_timeout, 30)
        self.assertEqual(new_con.connection_timeout, 1)

    def test_unconnected_ha_uses_replacement_dialog_and_restores_connections(
            self):
        """HA providers receive one override with every ROMMON pattern."""
        # Keep the patterns separate because real state patterns can contain
        # duplicate named groups that cannot be combined into one regex.
        device, con1 = self._build_device(r'(?P<loader>rommon)>')
        _, con2 = self._build_device(r'(?P<loader>switch):')
        device.is_ha = True
        device.connected = False
        con1.connected = False
        con2.connected = False
        con1_reply = con1.connect_reply
        con2_reply = con2.connect_reply

        parent = Mock()
        parent.mit = False
        parent.connection_timeout = 45
        parent.connect_reply = Dialog([
            Statement(pattern='parent custom prompt')
        ])
        parent.subconnections = [con1, con2]
        parent_reply = parent.connect_reply
        device.default = parent
        device.subconnections = [con1, con2]

        def _connect(connection_dialog, skip_initialization):
            self.assertTrue(skip_initialization)
            self.assertFalse(con1.mit)
            self.assertFalse(con2.mit)
            self.assertEqual(parent.connection_timeout, 45)
            self.assertEqual(con1.connection_timeout, 7)
            self.assertEqual(con2.connection_timeout, 7)
            self.assertIs(parent.connect_reply, parent_reply)
            break_statement = next(
                statement for statement in connection_dialog
                if statement.pattern == r'\.\.\.\.'
            )
            self.assertEqual(
                break_statement.args['rommon_patterns'],
                [r'(?P<loader>rommon)>', r'(?P<loader>switch):'],
            )
            self.assertIs(con1.connect_reply, con1_reply)
            self.assertIs(con2.connect_reply, con2_reply)
            con1.state_machine.update_cur_state('rommon')
            con2.state_machine.update_cur_state('rommon')

        parent.connect.side_effect = _connect

        send_break_boot(device, timeout=7)

        parent.connect.assert_called_once()
        device.connect.assert_not_called()
        self.assertIs(parent.connect_reply, parent_reply)
        self.assertIs(con1.connect_reply, con1_reply)
        self.assertIs(con2.connect_reply, con2_reply)
        self.assertFalse(parent.mit)
        self.assertFalse(con1.mit)
        self.assertFalse(con2.mit)
        self.assertEqual(parent.connection_timeout, 45)
        self.assertEqual(con1.connection_timeout, 30)
        self.assertEqual(con2.connection_timeout, 30)

    def test_unconnected_ha_validation_uses_redirected_subconnections(self):
        """State validation must not use old learned-plugin connections."""
        device, old_con1 = self._build_device(GenericPatterns().rommon_prompt)
        _, old_con2 = self._build_device(GenericPatterns().rommon_prompt)
        _, new_con1 = self._build_device(GenericPatterns().rommon_prompt)
        _, new_con2 = self._build_device(GenericPatterns().rommon_prompt)
        device.is_ha = True
        device.connected = False

        old_parent = Mock()
        old_parent.mit = False
        old_parent.subconnections = [old_con1, old_con2]
        new_parent = Mock()
        new_parent.mit = True
        new_parent.subconnections = [new_con1, new_con2]
        device.default = old_parent
        # Model a stale device-level reference to prove that the current
        # parent is authoritative after learned OS/token redirection.
        device.subconnections = [old_con1, old_con2]

        for con in (old_con1, old_con2):
            con.connection_timeout = 30
            con.state_machine.update_cur_state('enable')
        for con in (new_con1, new_con2):
            con.connection_timeout = 1
            con.state_machine.update_cur_state('rommon')

        def _connect(connection_dialog, skip_initialization):
            self.assertTrue(skip_initialization)
            device.default = new_parent

        old_parent.connect.side_effect = _connect

        send_break_boot(device, timeout=1)

        old_con1.sendline.assert_not_called()
        old_con2.sendline.assert_not_called()
        new_con1.sendline.assert_not_called()
        new_con2.sendline.assert_not_called()
        self.assertTrue(new_parent.mit)
        self.assertEqual(new_con1.connection_timeout, 1)
        self.assertEqual(new_con2.connection_timeout, 1)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_connected_breakboot_uses_replacement_dialog(
        self, mock_executor, mock_wait
    ):
        """Connected recovery must not run normal connection actions."""
        device, con = self._build_device()
        device.connection_provider.get_connection_dialog.return_value = \
            Dialog([
                generic_statements.press_return_stmt,
                generic_statements.hit_enter_stmt,
            ])
        normal_patterns = {
            generic_statements.press_return_stmt.pattern,
            generic_statements.hit_enter_stmt.pattern,
        }

        def match_replacement_dialog(patterns):
            self.assertTrue(normal_patterns.isdisjoint(
                statement.pattern for statement in patterns))
            return self._match_state('rommon')(patterns)

        con.spawn.match_buffer.side_effect = match_replacement_dialog
        self._setup_sync_executor(mock_executor, mock_wait)

        send_break_boot(device, timeout=1)

        device.connection_provider.get_connection_dialog.assert_not_called()
        self.assertEqual(con.state_machine.current_state, 'rommon')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_connected_breakboot_propagates_dialog_failure(
        self, mock_executor, mock_wait
    ):
        """A worker failure must not be hidden by the concurrent wrapper."""
        device, con = self._build_device()
        con.spawn.match_buffer.side_effect = RuntimeError(
            'state detection failed')
        self._setup_sync_executor(mock_executor, mock_wait)

        with self.assertRaisesRegex(RuntimeError, 'state detection failed'):
            send_break_boot(device, timeout=1)

        mock_executor.return_value.shutdown.assert_called_once_with(
            wait=True, cancel_futures=True)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_connected_breakboot_cancels_workers_after_timeout(
        self, mock_executor, mock_wait
    ):
        """Worker collection must remain bounded by the API timeout."""
        device, con1 = self._build_device()
        _, con2 = self._build_device()
        device.is_ha = True
        parent = Mock()
        parent.subconnections = [con1, con2]
        device.default = parent
        device.subconnections = [con1, con2]

        completed = Mock()
        unfinished = Mock()
        executor = mock_executor.return_value
        executor.submit.side_effect = [completed, unfinished]
        mock_wait.return_value = ({completed}, {unfinished})

        with self.assertRaisesRegex(
                SubCommandFailure,
                'Break boot timed out after 1 seconds for device uut'):
            send_break_boot(device, timeout=1)

        mock_wait.assert_called_once_with(
            [completed, unfinished], timeout=1,
            return_when=ALL_COMPLETED)
        completed.result.assert_called_once_with()
        unfinished.cancel.assert_called_once_with()
        unfinished.result.assert_not_called()
        executor.shutdown.assert_called_once_with(
            wait=True, cancel_futures=True)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_connected_breakboot_waits_for_running_worker_to_stop(
            self, mock_sleep):
        """No worker may continue sending after timeout is reported."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        con.alias = 'cli'
        con.spawn.buffer = '....'
        con.spawn.match_buffer.side_effect = self._match_buffer(con.spawn)
        con.spawn.trim_buffer.side_effect = self._trim_buffer(con.spawn)

        action_started = threading.Event()

        def blocking_sleep(_):
            action_started.set()
            threading.Event().wait(0.05)

        mock_sleep.side_effect = blocking_sleep

        with self.assertRaisesRegex(
                SubCommandFailure,
                'Break boot timed out after 1 seconds for device uut'):
            send_break_boot(device, break_count=100, timeout=1)

        self.assertTrue(action_started.is_set())
        sends_at_return = con.spawn.send.call_count
        threading.Event().wait(0.15)
        self.assertEqual(con.spawn.send.call_count, sends_at_return)
        con.spawn.close.assert_called_once_with()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_connected_breakboot_restores_credential_context(
        self, mock_executor, mock_wait
    ):
        """Temporary login credential selection does not leak after use."""
        device, con = self._build_device()
        con.context['login_creds'] = ['default']
        con.context['cred_list'] = ['existing']
        con.spawn.match_buffer.side_effect = self._match_state('rommon')
        self._setup_sync_executor(mock_executor, mock_wait)

        send_break_boot(device, timeout=1)

        self.assertEqual(con.context['cred_list'], ['existing'])

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.log.warning')
    def test_unconnected_device_preserves_learned_enable_state(self, mock_log):
        """An enable prompt learned by Unicon must not be forced to ROMMON."""
        device, con = self._build_device(GenericPatterns().rommon_prompt)
        device.connected = False
        con.connected = False
        con.state_machine.go_to = Mock()
        con.connect.side_effect = lambda connection_dialog, \
                skip_initialization: \
            con.state_machine.update_cur_state('enable')

        send_break_boot(device, timeout=1)

        self.assertEqual(con.state_machine.current_state, 'enable')
        self.assertTrue(con.connect.call_args.kwargs['skip_initialization'])
        con.sendline.assert_called_once_with()
        con.state_machine.go_to.assert_called_once_with(
            'any', spawn=con.spawn, context=con.context, timeout=1)
        mock_log.assert_called_once_with('The device uut is not in rommon')

if __name__ == '__main__':
    unittest.main()
