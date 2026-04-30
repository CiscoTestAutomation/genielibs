import unittest
from unittest.mock import MagicMock, patch

from genie.libs.clean.exception import FailedToBootException
from genie.libs.sdk.apis.iosxe.rommon.utils import device_rommon_boot


class TestDeviceRommonBoot(unittest.TestCase):

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    def test_device_rommon_boot_failure_when_still_in_rommon(self, mock_wait, mock_executor):

        # Mock device and its API
        device = MagicMock()
        device.name = 'uut'
        device.is_ha = False
        device.default = MagicMock()
        # Ensure conn_list resolves to [device.default]
        device.subconnections = None
        device.clean = {'device_recovery': {'timeout': 2000}}

        # Recovery info: simulate tftp path (we only need cmd to be set)
        device.api.get_recovery_details.return_value = {
            'golden_image': [],
            'tftp_image': ['dummy'],
            'tftp_boot': {'image': ['dummy_image'], 'tftp_server': '1.1.1.1'},
        }
        device.api.get_tftp_boot_command.return_value = ('boot_cmd', 'dummy_image')

        # conn_list -> [device.default]
        conn = device.default
        conn.context = {}
        state_machine = MagicMock()
        # Simulate that after the boot attempt, device is still in rommon
        state_machine.current_state = 'rommon'
        conn.state_machine = state_machine

        # ThreadPoolExecutor mock: execute submitted task immediately
        executor_instance = MagicMock()
        def _submit(fn, *args, **kwargs):
            fn(*args, **kwargs)
            future = MagicMock()
            return future
        executor_instance.submit.side_effect = _submit
        mock_executor.return_value = executor_instance

        with self.assertRaises(FailedToBootException):
            device_rommon_boot(device)

        # Ensure we actually checked state_machine.current_state
        self.assertTrue(hasattr(conn, 'state_machine'))
        self.assertEqual(conn.state_machine.current_state, 'rommon')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    def test_device_rommon_boot_success_when_not_in_rommon(self, mock_wait, mock_executor):

        device = MagicMock()
        device.name = 'uut'
        device.is_ha = False
        device.default = MagicMock()
        # Ensure conn_list resolves to [device.default]
        device.subconnections = None
        device.clean = {'device_recovery': {'timeout': 2000}}

        device.api.get_recovery_details.return_value = {
            'golden_image': ['golden.bin'],
            'tftp_image': [],
            'tftp_boot': {},
        }

        # Mock the ignore startup config APIs
        device.api.unconfigure_ignore_startup_config.return_value = None
        device.api.verify_ignore_startup_config.return_value = False

        conn = device.default
        conn.context = {}
        state_machine = MagicMock()
        # Simulate that after the boot attempt, device has left rommon
        state_machine.current_state = 'disable'
        conn.state_machine = state_machine

        executor_instance = MagicMock()
        def _submit(fn, *args, **kwargs):
            fn(*args, **kwargs)
            future = MagicMock()
            return future
        executor_instance.submit.side_effect = _submit
        mock_executor.return_value = executor_instance

        # Should not raise when state is not rommon
        device_rommon_boot(device)

        # Verify we reached the post-boot path (enable/init/credentials)
        device.enable.assert_called_once()
        device.connection_provider.init_connection.assert_called_once()
        device.api.configure_management_credentials.assert_called_once()
        device.api.unconfigure_ignore_startup_config.assert_called_once()
        device.api.verify_ignore_startup_config.assert_called_once()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    def test_rommon_switch_boot_max_attempts(self, mock_wait, mock_executor, mock_sleep):
        """Verify _rommon_switch_boot sends boot command up to MAX_BOOT_ATTEMPTS
        times, then raises Exception on the next call."""

        device = MagicMock()
        device.name = 'uut'
        device.is_ha = False
        device.default = MagicMock()
        device.subconnections = None
        device.clean = {'device_recovery': {'timeout': 2000}}
        device.api.verify_ignore_startup_config.return_value = False
        device.api.get_recovery_details.return_value = {
            'golden_image': ['golden.bin'],
            'tftp_image': [],
            'tftp_boot': {},
        }

        conn = device.default
        conn.context = {}
        state_machine = MagicMock()
        state_machine.current_state = 'disable'
        conn.state_machine = state_machine

        executor_instance = MagicMock()
        def _submit(fn, *args, **kwargs):
            fn(*args, **kwargs)
            return MagicMock()
        executor_instance.submit.side_effect = _submit
        mock_executor.return_value = executor_instance

        device_rommon_boot(device)
        _, go_to_kwargs = conn.state_machine.go_to.call_args
        dialog = go_to_kwargs.get('dialog')
        handler = None
        for stmt in dialog:
            if getattr(getattr(stmt, 'action', None), '__name__', '') == '_rommon_switch_boot':
                handler = stmt.action
                break
        self.assertIsNotNone(handler, "Could not find _rommon_switch_boot in dialog")
        spawn = MagicMock()
        spawn.settings.MAX_BOOT_ATTEMPTS = 3
        session = {}
        context = {'image_to_boot': 'tftp:'}

        for i in range(3):
            handler(spawn, session, context)
        self.assertEqual(session['boot_attempt_count'], 3)
        self.assertEqual(spawn.sendline.call_count, 3)
        spawn.sendline.assert_called_with('boot tftp:')
        with self.assertRaises(Exception) as cm:
            handler(spawn, session, context)
        self.assertIn('Too many failed boot attempts', str(cm.exception))

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_device_rommon_boot_ha_sync_to_rommon(self, mocke_sleep, mock_wait, mock_executor):
        """Verify that HA device syncs non-rommon subconnections to rommon before proceeding"""

        device = MagicMock()
        device.name = 'ha_device'
        device.is_ha = True
        device.clean = {'device_recovery': {'timeout': 2000}}

        device.connection_provider = MagicMock()

        conn1 = MagicMock()
        conn1.alias = 'a'
        conn1.state_machine.current_state = 'rommon'
        conn1.context = {}

        conn2 = MagicMock()
        conn2.alias = 'b'
        conn2.state_machine.current_state = 'enable'
        conn2.context = {}

        device.subconnections = [conn1, conn2]

        device.api.get_recovery_details.return_value = {
            'golden_image': ['golden.bin'],
            'tftp_image': [],
            'tftp_boot': {},
        }
        device.api.verify_ignore_startup_config.return_value = False


        def device_rommon_side_effect():
            for con in device.subconnections:
                con.state_machine.current_state = 'rommon'
        
        device.rommon.side_effect = device_rommon_side_effect

        def execute_task(fn, *args, **kwargs):
            fn(*args, **kwargs)
            return MagicMock()

        mock_executor.return_value.submit.side_effect = execute_task
        mock_executor.return_value.__enter__.return_value = mock_executor.return_value
        
        conn1.state_machine.go_to.side_effect = lambda *a, **k: setattr(conn1.state_machine, 'current_state', 'disable')
        conn2.state_machine.go_to.side_effect = lambda *a, **k: setattr(conn2.state_machine, 'current_state', 'disable')

        from genie.libs.sdk.apis.iosxe.rommon.utils import device_rommon_boot
        device_rommon_boot(device)

        device.rommon.assert_called_once()
        device.connection_provider.designate_handles.assert_called_once()
        self.assertGreaterEqual(mock_wait.call_count, 1)


if __name__ == '__main__':
    unittest.main()
