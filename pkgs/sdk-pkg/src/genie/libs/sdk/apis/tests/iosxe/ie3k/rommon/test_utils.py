import unittest
import threading
from time import perf_counter
from unittest.mock import MagicMock, patch
from concurrent.futures import Future

from unicon import Connection
from unicon.plugins.tests.mock.mock_device_iosxe import (
    MockDeviceTcpWrapperIOSXE,
)

from genie.libs.clean.exception import FailedToBootException
from genie.libs.sdk.apis.iosxe.ie3k.rommon.utils import device_rommon_boot


class TestIe3kDeviceRommonBoot(unittest.TestCase):

    def _build_device(self, images, max_boot_attempts=3):
        device = MagicMock()
        device.name = 'uut'
        device.is_ha = False
        device.clean = {'device_recovery': {'timeout': 120}}

        conn = MagicMock()
        conn.alias = 'con1'
        conn.context = {}
        conn.spawn = MagicMock()
        conn.spawn.settings.MAX_BOOT_ATTEMPTS = max_boot_attempts
        conn.spawn.sendline = MagicMock()
        conn.state_machine = MagicMock()
        conn.state_machine.current_state = 'rommon'
        conn.state_machine.learn_hostname = False
        conn.learn_hostname = False
        conn.learned_hostname = None

        device.default = conn
        device.subconnections = None
        device.api.get_recovery_details.return_value = {'golden_image': images}
        return device, conn

    def _setup_sync_executor(self, mock_executor, mock_wait):
        executor_instance = MagicMock()

        def _submit(fn, *args, **kwargs):
            future = Future()
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                future.set_exception(exc)
            else:
                future.set_result(result)
            return future

        executor_instance.submit.side_effect = _submit
        mock_executor.return_value = executor_instance
        mock_wait.side_effect = lambda futures, timeout, return_when: (set(futures), set())
        return executor_instance

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_single_image_normal_from_get_recovery_details(self, mock_executor, mock_wait, _):
        device, conn = self._build_device(['flash:image1.bin'])

        def _go_to_disable(*args, **kwargs):
            conn.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = _go_to_disable
        self._setup_sync_executor(mock_executor, mock_wait)

        device_rommon_boot(device)

        device.api.get_recovery_details.assert_called_once_with(None, None)
        device.api.execute_rommon_reset.assert_called_once_with()
        device.enable.assert_called_once_with()
        device.connection_provider.init_connection.assert_called_once_with()
        device.api.configure_management_credentials.assert_called_once_with()
        device.api.execute_write_memory.assert_called_once_with()
        conn.state_machine.go_to.assert_called_once()
        conn.connection_provider.learn_hostname.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.sleep')
    def test_rommon_boot_learns_mismatched_hostname(self, _):
        configured_hostname = 'IE-3300-8U2X-4MU-uut3-st2-ipo'
        actual_hostname = 'IE-3300-8U2X-4MU-uut3'
        image = 'flash:ie3x00-universalk9.bin'
        username = 'admin'
        password = 'test-password'

        mock_device = MockDeviceTcpWrapperIOSXE(
            port=0,
            state='cat3k_rommon',
            hostname=actual_hostname,
        )
        rommon_commands = mock_device.mockdevice.mock_data[
            'cat3k_rommon']['commands']
        boot = rommon_commands['boot flash:rp_super_universalk9.edison.bin']
        boot['response'] = 'Booting IOS-XE\r\n'
        boot['new_state'] = 'cat3k_return_to_get_started'
        boot.pop('timing', None)
        rommon_commands[f'boot {image}'] = boot
        mock_device.mockdevice.mock_data[
            'cat3k_return_to_get_started']['commands'][''][
                'new_state'] = 'cat3k_login'
        mock_device.mockdevice.mock_data['cat3k_login']['commands'] = {
            username: {'new_state': 'cat3k_password'}
        }
        mock_device.mockdevice.mock_data['cat3k_password']['commands'] = {
            password: {'new_state': 'cat3k_exec'}
        }
        mock_device.start()

        connection = Connection(
            hostname=configured_hostname,
            start=['telnet 127.0.0.1 {}'.format(mock_device.ports[0])],
            os='iosxe',
            platform='ie3k',
            credentials={
                'default': {
                    'username': username,
                    'password': password,
                },
            },
            image_to_boot=image,
            connection_timeout=5,
            log_buffer=True,
            log_stdout=False,
            mit=True,
            learn_hostname=True,
        )

        try:
            connection.connect()
            self.assertEqual(connection.state_machine.current_state, 'rommon')

            sent = []
            sendline = connection.spawn.sendline

            def _record_sendline(command=''):
                sent.append(command)
                return sendline(command)

            connection.spawn.sendline = _record_sendline

            device = MagicMock()
            device.name = configured_hostname
            device.is_ha = False
            device.clean = {'device_recovery': {'timeout': 5}}
            device.default = connection
            device.subconnections = None
            device.connection_provider = connection.connection_provider
            device.enable = connection.enable
            device.api.get_recovery_details.return_value = {
                'golden_image': [image]
            }

            with patch.object(
                connection.connection_provider,
                'init_connection',
                wraps=connection.connection_provider.init_connection,
            ) as init_connection:
                device_rommon_boot(device, timeout=5)

            self.assertIn(username, sent)
            self.assertIn(password, sent)
            self.assertIn('Username:', connection.log_buffer)
            self.assertIn('Password:', connection.log_buffer)
            self.assertIn(f'{actual_hostname}>', connection.log_buffer)
            self.assertEqual(connection.learned_hostname, actual_hostname)
            self.assertEqual(connection.state_machine.current_state, 'enable')
            self.assertFalse(connection.state_machine.learn_hostname)
            init_connection.assert_called_once_with()
        finally:
            connection.disconnect()
            mock_device.stop()

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_hostname_learning_restored_after_failed_images(
        self, mock_executor, mock_wait
    ):
        images = ['flash:image1.bin', 'flash:image2.bin']
        device, conn = self._build_device(images)
        conn.learn_hostname = True
        conn.state_machine.learn_hostname = True
        attempted_images = []

        def _go_to_fail(*args, **kwargs):
            self.assertTrue(conn.state_machine.learn_hostname)
            attempted_images.append(kwargs['context']['boot_cmd'])
            raise Exception('boot failed')

        conn.state_machine.go_to.side_effect = _go_to_fail
        self._setup_sync_executor(mock_executor, mock_wait)

        with self.assertRaises(FailedToBootException):
            device_rommon_boot(device, timeout=120)

        self.assertEqual(
            attempted_images,
            [f'boot {image}' for image in images],
        )
        self.assertTrue(conn.state_machine.learn_hostname)
        conn.connection_provider.learn_hostname.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_hostname_learning_restored_when_learning_fails(
        self, mock_executor, mock_wait
    ):
        device, conn = self._build_device(['flash:image.bin'])
        conn.learn_hostname = True

        def _go_to_disable(*args, **kwargs):
            self.assertTrue(conn.state_machine.learn_hostname)
            conn.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = _go_to_disable
        conn.connection_provider.learn_hostname.side_effect = Exception(
            'hostname learning failed'
        )
        self._setup_sync_executor(mock_executor, mock_wait)

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device, timeout=120)

        self.assertIn('hostname learning failed', str(cm.exception))
        self.assertFalse(conn.state_machine.learn_hostname)
        self.assertIsNone(conn.context['boot_cmd'])

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_ha_hostname_learning_uses_device_provider(
        self, mock_executor, mock_wait, _
    ):
        device, conn = self._build_device(['flash:image.bin'])
        device.is_ha = True
        device.subconnections = [conn]
        conn.learn_hostname = True

        def _go_to_disable(*args, **kwargs):
            self.assertTrue(conn.state_machine.learn_hostname)
            conn.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = _go_to_disable
        self._setup_sync_executor(mock_executor, mock_wait)

        device_rommon_boot(device, timeout=120)

        device.connection_provider.learn_hostname.assert_called_once_with(conn)
        conn.connection_provider.learn_hostname.assert_not_called()
        self.assertFalse(conn.state_machine.learn_hostname)

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_single_image_failure(self, mock_executor, mock_wait):
        device, conn = self._build_device(['flash:image1.bin'])
        conn.state_machine.go_to.side_effect = Exception('image boot failed')
        self._setup_sync_executor(mock_executor, mock_wait)

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device)

        self.assertIn('All golden images exhausted', str(cm.exception))
        self.assertIn('Last error: image boot failed', str(cm.exception))

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_full_timeout_without_exhausting_all_images(self, mock_executor, mock_wait):
        device, conn = self._build_device(['flash:image1.bin', 'flash:image2.bin'])

        executor_instance = MagicMock()
        future = MagicMock()
        executor_instance.submit.return_value = future
        mock_executor.return_value = executor_instance
        mock_wait.return_value = (set(), {future})

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device, timeout=7)

        self.assertIn('Timeout expired after 7 seconds', str(cm.exception))
        conn.state_machine.go_to.assert_not_called()

    def test_timeout_with_real_executor_and_wait_path(self):
        """Exercise real ThreadPoolExecutor + wait_futures timeout behavior once."""
        device, conn = self._build_device(['flash:image1.bin'])
        block_event = threading.Event()

        def _blocking_go_to(*args, **kwargs):
            # Keep worker busy long enough for wait_futures timeout to fire.
            block_event.wait(5)

        conn.state_machine.go_to.side_effect = _blocking_go_to

        start = perf_counter()
        try:
            with self.assertRaises(FailedToBootException) as cm:
                device_rommon_boot(device, timeout=0.1)
        finally:
            # Release background worker promptly after assertion.
            block_event.set()

        elapsed = perf_counter() - start
        self.assertIn('Timeout expired after 0.1 seconds', str(cm.exception))
        self.assertGreaterEqual(elapsed, 0.08)
        self.assertLess(elapsed, 1.5)

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_second_image_selected_after_first_reaches_max_attempts(
        self, mock_executor, mock_wait, _
    ):
        image1 = 'flash:image1.bin'
        image2 = 'flash:image2.bin'
        device, conn = self._build_device([image1, image2], max_boot_attempts=3)

        attempted_images = []

        def _go_to_side_effect(*args, **kwargs):
            context = kwargs['context']
            dialog = kwargs['dialog']
            attempted_images.append(context['boot_cmd'])

            handler = None
            for stmt in dialog:
                action = getattr(stmt, 'action', None)
                if getattr(action, '__name__', '') == '_rommon_switch_boot':
                    handler = action
                    break

            if context['boot_cmd'] == f'boot {image1}':
                session = {}
                for _ in range(conn.spawn.settings.MAX_BOOT_ATTEMPTS):
                    handler(conn.spawn, session, context)
                with self.assertRaises(Exception):
                    handler(conn.spawn, session, context)
                conn.state_machine.current_state = 'rommon'
                raise Exception('first image failed')

            conn.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = _go_to_side_effect
        self._setup_sync_executor(mock_executor, mock_wait)

        device_rommon_boot(device)

        self.assertEqual(attempted_images[:2], [f'boot {image1}', f'boot {image2}'])
        self.assertEqual(
            conn.spawn.sendline.call_count,
            conn.spawn.settings.MAX_BOOT_ATTEMPTS - 1,
        )
        conn.spawn.sendline.assert_called_with(f'boot {image1}')

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_all_images_exhausted_before_timeout(self, mock_executor, mock_wait):
        images = ['flash:image1.bin', 'flash:image2.bin']
        device, conn = self._build_device(images)
        attempted_images = []

        def _go_to_fail(*args, **kwargs):
            attempted_images.append(kwargs['context']['boot_cmd'])
            conn.state_machine.current_state = 'rommon'
            raise Exception('boot failed')

        conn.state_machine.go_to.side_effect = _go_to_fail
        self._setup_sync_executor(mock_executor, mock_wait)

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device, timeout=120)

        self.assertEqual(attempted_images, [f'boot {image}' for image in images])
        self.assertIn('All golden images exhausted', str(cm.exception))
        self.assertNotIn('Timeout expired', str(cm.exception))

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_completed_future_exception_is_raised(self, mock_executor, mock_wait):
        device, conn = self._build_device(['flash:image1.bin'])
        conn.state_machine.current_state = 'disable'

        future = Future()
        future.set_exception(Exception('worker failed after state changed'))

        executor_instance = MagicMock()
        executor_instance.submit.return_value = future
        mock_executor.return_value = executor_instance
        mock_wait.return_value = ({future}, set())

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device, timeout=120)

        self.assertIn('worker failed after state changed', str(cm.exception))

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.monotonic')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_does_not_retry_after_overall_deadline_expires(
        self, mock_executor, mock_wait, mock_monotonic
    ):
        images = ['flash:image1.bin', 'flash:image2.bin']
        device, conn = self._build_device(images)
        attempted_images = []

        # First call computes deadline; second is remaining time before image1;
        # third indicates the overall deadline has already expired before image2.
        mock_monotonic.side_effect = [100.0, 100.0, 107.1]

        def _go_to_fail(*args, **kwargs):
            attempted_images.append(kwargs['context']['boot_cmd'])
            conn.state_machine.current_state = 'rommon'
            raise Exception('boot failed')

        conn.state_machine.go_to.side_effect = _go_to_fail
        self._setup_sync_executor(mock_executor, mock_wait)

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device, timeout=7)

        self.assertEqual(attempted_images, ['boot flash:image1.bin'])
        self.assertIn('Overall timeout expired before booting image', str(cm.exception))

    def test_no_image_exception(self):
        device, conn = self._build_device([])
        attempted_commands = []

        def _go_to_fail(*args, **kwargs):
            attempted_commands.append(kwargs['context']['boot_cmd'])
            conn.state_machine.current_state = 'rommon'
            raise Exception('default boot failed')

        conn.state_machine.go_to.side_effect = _go_to_fail

        with self.assertLogs(
            'genie.libs.sdk.apis.iosxe.ie3k.rommon.utils', level='WARNING'
        ) as logs, self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device)

        output = '\n'.join(logs.output)
        self.assertEqual(attempted_commands, ['boot'])
        self.assertIn(
            "Default ROMMON 'boot' command failed for connection 'con1'",
            str(cm.exception)
        )
        self.assertIn('Last error: default boot failed', str(cm.exception))
        self.assertNotIn("image 'None'", output)
        self.assertNotIn('Trying next image.', output)
        self.assertNotIn('All golden images exhausted', str(cm.exception))
        device.api.get_recovery_details.assert_called_once_with(None, None)

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_no_image_default_boot_success(
        self, mock_executor, mock_wait, _
    ):
        device, conn = self._build_device([])
        attempted_commands = []

        def _go_to_disable(*args, **kwargs):
            attempted_commands.append(kwargs['context']['boot_cmd'])
            conn.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = _go_to_disable
        self._setup_sync_executor(mock_executor, mock_wait)

        device_rommon_boot(device)

        self.assertEqual(attempted_commands, ['boot'])
        device.enable.assert_called_once_with()

    def test_no_image_without_boot_exception_reports_rommon_state(self):
        device, _ = self._build_device([])

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device)

        self.assertIn(
            'Last error: Connection remained in rommon after boot attempt',
            str(cm.exception)
        )
        self.assertNotIn('Last error: None', str(cm.exception))

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.monotonic')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_no_image_timeout_error_reporting(
        self, mock_executor, mock_wait, mock_monotonic
    ):
        device, conn = self._build_device([])
        mock_monotonic.side_effect = [100.0, 100.0]
        self._setup_sync_executor(mock_executor, mock_wait)

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device, timeout=0)

        self.assertIn(
            "Overall timeout expired before default ROMMON 'boot' command",
            str(cm.exception)
        )
        self.assertNotIn("image 'None'", str(cm.exception))
        conn.state_machine.go_to.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_uses_provided_golden_image_argument(self, mock_executor, mock_wait, _):
        provided = ['flash:provided.bin']
        device, conn = self._build_device(provided)

        booted_images = []

        def _go_to_disable(*args, **kwargs):
            booted_images.append(kwargs['context']['boot_cmd'])
            conn.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = _go_to_disable
        self._setup_sync_executor(mock_executor, mock_wait)

        device_rommon_boot(device, golden_image=provided)

        device.api.get_recovery_details.assert_called_once_with(provided, None)
        self.assertEqual(booted_images, ['boot flash:provided.bin'])

    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.wait_futures')
    @patch('genie.libs.sdk.apis.iosxe.ie3k.rommon.utils.ThreadPoolExecutor')
    def test_ordered_retry_across_second_third_n_image(self, mock_executor, mock_wait, _):
        images = [
            'flash:image1.bin',
            'flash:image2.bin',
            'flash:image3.bin',
            'flash:image4.bin',
        ]
        device, conn = self._build_device(images)
        attempted_images = []

        def _go_to_side_effect(*args, **kwargs):
            boot_cmd = kwargs['context']['boot_cmd']
            attempted_images.append(boot_cmd)

            # Fail first N-1 images, succeed on the Nth image.
            if boot_cmd != f'boot {images[-1]}':
                conn.state_machine.current_state = 'rommon'
                raise Exception(f'failed on {boot_cmd}')

            conn.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = _go_to_side_effect
        self._setup_sync_executor(mock_executor, mock_wait)

        device_rommon_boot(device)

        self.assertEqual(attempted_images, [f'boot {image}' for image in images])
        self.assertEqual(conn.state_machine.go_to.call_count, len(images))


if __name__ == '__main__':
    unittest.main()
