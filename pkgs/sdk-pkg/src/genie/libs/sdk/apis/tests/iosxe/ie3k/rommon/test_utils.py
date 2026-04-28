import unittest
import threading
from time import perf_counter
from unittest.mock import MagicMock, patch
from concurrent.futures import Future

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
        device, _ = self._build_device([])

        with self.assertRaises(FailedToBootException) as cm:
            device_rommon_boot(device)

        self.assertIn('All golden images exhausted', str(cm.exception))
        device.api.get_recovery_details.assert_called_once_with(None, None)

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
