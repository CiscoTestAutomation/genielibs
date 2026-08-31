import unittest
from unittest.mock import MagicMock, call, patch

from genie.libs.sdk.apis.iosxe.utils import recover_device_to_enable_state


class TestRecoverDeviceToEnableState(unittest.TestCase):

    @patch('genie.libs.sdk.apis.iosxe.utils.log')
    def test_reconnects_when_session_dropped(self, mock_log):
        device = MagicMock()
        device.is_connected.return_value = False
        device.state_machine.current_state = 'enable'

        recover_device_to_enable_state(device, timeout=150)

        # A stale session must be torn down before reconnecting.
        device.disconnect.assert_called_once_with()
        device.connect.assert_called_once_with()
        self.assertLess(
            device.mock_calls.index(call.disconnect()),
            device.mock_calls.index(call.connect()),
        )
        device.state_machine.go_to.assert_called_once_with(
            'any', device.spawn, timeout=150, prompt_recovery=True)

    @patch('genie.libs.sdk.apis.iosxe.utils.log')
    def test_reconnect_continues_when_disconnect_fails(self, mock_log):
        device = MagicMock()
        device.is_connected.return_value = False
        device.disconnect.side_effect = Exception('already disconnected')
        device.state_machine.current_state = 'enable'

        recover_device_to_enable_state(device, timeout=150)

        # A failed disconnect must not stop the reconnect attempt.
        device.connect.assert_called_once_with()
        # The API logs at debug level only, leaving user facing logging
        # to the caller.
        mock_log.warning.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.utils.log')
    def test_skips_reconnect_when_session_alive(self, mock_log):
        device = MagicMock()
        device.is_connected.return_value = True
        device.state_machine.current_state = 'enable'

        recover_device_to_enable_state(device, timeout=150)

        device.disconnect.assert_not_called()
        device.connect.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.utils.log')
    def test_sends_line_before_detecting_state(self, mock_log):
        device = MagicMock()
        device.is_connected.return_value = True
        device.state_machine.current_state = 'enable'

        recover_device_to_enable_state(device, timeout=150)

        # An empty line is required so an idle session produces a prompt
        # for the state machine to match against.
        device.sendline.assert_called_once_with()
        self.assertLess(
            device.mock_calls.index(call.sendline()),
            device.mock_calls.index(
                call.state_machine.go_to(
                    'any', device.spawn, timeout=150,
                    prompt_recovery=True)),
        )

    @patch('genie.libs.sdk.apis.iosxe.utils.log')
    def test_recovers_from_login_prompt_to_enable(self, mock_log):
        device = MagicMock()
        device.is_connected.return_value = True
        states = iter(['user_exec', 'enable'])

        def _go_to(target_state, spawn, **kwargs):
            device.state_machine.current_state = next(states)

        device.state_machine.go_to.side_effect = _go_to

        recover_device_to_enable_state(device, timeout=150)

        self.assertEqual(
            [
                call('any', device.spawn, timeout=150,
                     prompt_recovery=True),
                call('enable', device.spawn, timeout=150,
                     prompt_recovery=True),
            ],
            device.state_machine.go_to.call_args_list,
        )
        self.assertEqual('enable', device.state_machine.current_state)

    @patch('genie.libs.sdk.apis.iosxe.utils.log')
    def test_raises_when_device_in_rommon(self, mock_log):
        device = MagicMock()
        device.is_connected.return_value = True
        device.state_machine.current_state = 'rommon'

        with self.assertRaises(RuntimeError):
            recover_device_to_enable_state(device, timeout=150)

        # Never attempt an enable transition from ROMMON.
        device.state_machine.go_to.assert_called_once_with(
            'any', device.spawn, timeout=150, prompt_recovery=True)

    @patch('genie.libs.sdk.apis.iosxe.utils.log')
    def test_raises_when_enable_not_reached(self, mock_log):
        device = MagicMock()
        device.is_connected.return_value = True
        device.state_machine.current_state = 'user_exec'

        with self.assertRaises(RuntimeError):
            recover_device_to_enable_state(device, timeout=150)


if __name__ == '__main__':
    unittest.main()
