from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ie3k.execute import execute_rommon_reset


class TestExecuteRommonReset(TestCase):

    def test_execute_rommon_reset_only_on_rommon_connections(self):
        device = Mock()
        device.name = "ie3k"

        rommon_conn = Mock()
        rommon_conn.state_machine = Mock()
        rommon_conn.state_machine.current_state = "rommon"

        enable_conn = Mock()
        enable_conn.state_machine = Mock()
        enable_conn.state_machine.current_state = "enable"

        device.subconnections = [rommon_conn, enable_conn]

        result = execute_rommon_reset(device, timeout=123)

        rommon_conn.execute.assert_called_once()
        call_args, call_kwargs = rommon_conn.execute.call_args
        self.assertEqual(call_args[0], "reset")
        self.assertEqual(call_kwargs["timeout"], 123)
        self.assertIn("reply", call_kwargs)

        enable_conn.execute.assert_not_called()
        self.assertIsNone(result)