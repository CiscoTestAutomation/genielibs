import unittest
from unittest.mock import MagicMock, call

from genie.libs.sdk.apis.execute import execute_clear_line


class TestExecuteClearLine(unittest.TestCase):

    def test_execute_clear_line_uses_mapped_terminal_server_lines(self):
        terminal_server = MagicMock(name='terminal_server')
        device = MagicMock(name='device')
        device.name = 'device'
        device.peripherals = {
            'terminal_server': {'terminal_server': [7, 8]}}
        device.testbed.devices = {'terminal_server': terminal_server}

        result = execute_clear_line(device)

        self.assertIsNone(result)
        terminal_server.connect.assert_called_once_with(
            init_exec_commands=[], init_config_commands=[])
        self.assertEqual([
            call('clear line 7'),
            call('clear line 8'),
        ], terminal_server.execute.call_args_list)
        terminal_server.destroy.assert_called_once_with()
        device.disconnect.assert_called_once_with(alias='cli')
        device.connect.assert_not_called()
        device.execute.assert_not_called()
