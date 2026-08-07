import unittest
from unittest.mock import Mock, ANY, call

from genie.libs.sdk.apis.iosxe.platform.execute import execute_write_memory
from unicon.core.errors import SubCommandFailure
from unicon.plugins.iosxe.service_statements import proceed_confirm_stmt


class TestExecuteWriteMemory(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_execute_write_memory_autonomous(self):
        self.device.execute.side_effect = [
            'Router operating mode: Autonomous',
            'Building configuration...\n[OK]',
        ]

        execute_write_memory(self.device)

        self.device.execute.assert_has_calls([
            call('show version | include operating mode'),
            call('write memory', reply=ANY, timeout=300),
        ])
        self.assertEqual(2, self.device.execute.call_count)
        self.device.parse.assert_not_called()
        self.device.configure.assert_not_called()

    def test_execute_write_memory_controller_managed(self):
        self.device.execute.side_effect = [
            'Router operating mode: Controller-Managed',
            {
                'config-transaction': '',
                'commit': 'Commit complete.',
                'end': '',
            },
        ]

        execute_write_memory(self.device, timeout=600)

        self.device.execute.assert_has_calls([
            call('show version | include operating mode'),
            call(
                ['config-transaction', 'commit', 'end'],
                allow_state_change=True,
                service_dialog=ANY,
                timeout=600),
        ])
        self.assertEqual(2, self.device.execute.call_count)
        commit_dialog = self.device.execute.call_args_list[1].kwargs[
            'service_dialog']
        self.assertIs(
            proceed_confirm_stmt, commit_dialog.statement_list[0])
        self.device.parse.assert_not_called()
        self.device.configure.assert_not_called()

    def test_execute_write_memory_controller_no_modifications(self):
        self.device.execute.side_effect = [
            'operating mode: Controller-Managed',
            {
                'config-transaction': '',
                'commit': '% No modifications to commit.',
                'end': '',
            },
        ]

        execute_write_memory(self.device)

        self.device.execute.assert_has_calls([
            call('show version | include operating mode'),
            call(
                ['config-transaction', 'commit', 'end'],
                allow_state_change=True,
                service_dialog=ANY,
                timeout=300),
        ])

    def test_execute_write_memory_controller_commit_warning(self):
        self.device.execute.side_effect = [
            'Router operating mode: Controller-Managed',
            {
                'config-transaction': '',
                'commit': (
                    'The following warnings were generated:\n'
                    'Proceed? [yes,no]'),
                'end': '',
            },
        ]

        execute_write_memory(self.device)

        self.device.execute.assert_has_calls([
            call('show version | include operating mode'),
            call(
                ['config-transaction', 'commit', 'end'],
                allow_state_change=True,
                service_dialog=ANY,
                timeout=300),
        ])

    def test_execute_write_memory_missing_operating_mode(self):
        self.device.execute.side_effect = [
            '',
            'Building configuration...\n[OK]',
        ]

        execute_write_memory(self.device)

        self.device.execute.assert_has_calls([
            call('show version | include operating mode'),
            call('write memory', reply=ANY, timeout=300),
        ])

    def test_execute_write_memory_unknown_operating_mode(self):
        self.device.execute.side_effect = [
            'Router operating mode: Unknown',
            'Building configuration...\n[OK]',
        ]

        execute_write_memory(self.device)

        self.device.execute.assert_has_calls([
            call('show version | include operating mode'),
            call('write memory', reply=ANY, timeout=300),
        ])

    def test_execute_write_memory_detection_failure(self):
        error = SubCommandFailure('mode query failed')
        self.device.execute.side_effect = error

        with self.assertRaises(SubCommandFailure) as context:
            execute_write_memory(self.device)

        self.assertIs(error, context.exception)
        self.device.execute.assert_called_once_with(
            'show version | include operating mode')

    def test_execute_write_memory_unsupported_output(self):
        self.device.execute.side_effect = [
            'Router operating mode: Autonomous',
            'This command is not supported in Controller mode.',
        ]

        with self.assertRaises(Exception):
            execute_write_memory(self.device)

        self.device.configure.assert_not_called()

    def test_execute_write_memory_commit_unsupported_output(self):
        self.device.execute.side_effect = [
            'Router operating mode: Controller-Managed',
            {
                'config-transaction': '',
                'commit': 'Commit failed.',
                'end': '',
            },
        ]

        with self.assertRaisesRegex(Exception, 'Commit failed'):
            execute_write_memory(self.device)

        self.device.execute.assert_has_calls([
            call('show version | include operating mode'),
            call(
                ['config-transaction', 'commit', 'end'],
                allow_state_change=True,
                service_dialog=ANY,
                timeout=300),
        ])

    def test_execute_write_memory_commit_failure(self):
        error = SubCommandFailure('commit failed')
        self.device.execute.side_effect = [
            'Router operating mode: Controller-Managed',
            error,
        ]

        with self.assertRaises(SubCommandFailure) as context:
            execute_write_memory(self.device)

        self.assertIs(error, context.exception)

    def test_execute_write_memory_commit_timeout(self):
        error = TimeoutError('commit timeout')
        self.device.execute.side_effect = [
            'Router operating mode: Controller-Managed',
            error,
        ]

        with self.assertRaises(TimeoutError) as context:
            execute_write_memory(self.device, timeout=900)

        self.assertIs(error, context.exception)
        self.device.execute.assert_has_calls([
            call('show version | include operating mode'),
            call(
                ['config-transaction', 'commit', 'end'],
                allow_state_change=True,
                service_dialog=ANY,
                timeout=900),
        ])


if __name__ == '__main__':
    unittest.main()
