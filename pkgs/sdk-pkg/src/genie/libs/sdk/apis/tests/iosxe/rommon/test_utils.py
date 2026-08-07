import unittest
from concurrent.futures import Future
from types import SimpleNamespace
from unittest.mock import Mock, patch

from unicon.eal.dialogs import Dialog
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
                raise
            else:
                future.set_result(result)
            return future

        executor.submit.side_effect = _submit
        mock_executor.return_value = executor
        mock_wait.side_effect = lambda futures, timeout, return_when: \
            (set(futures), set())

    def _build_device(self):
        class RommonStateMachine(StateMachine):
            def create(self):
                self.add_state(State('generic', 'generic>'))
                self.add_state(State('rommon', 'rommon>'))

        device = Mock()
        device.name = 'uut'
        device.is_ha = False
        device.connected = True
        device.credentials = {}
        device.connection_provider.get_connection_dialog.return_value = \
            Dialog()

        conn = Mock()
        conn.context = {}
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
            'any', spawn=con.spawn, context=con.context)
        self.assertEqual(con.state_machine.current_state, 'rommon')


if __name__ == '__main__':
    unittest.main()
