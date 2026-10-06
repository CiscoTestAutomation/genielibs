from unittest import TestCase
from unittest.mock import ANY, MagicMock, call, patch

from genie.libs.sdk.apis.nxos.platform.execute import delete_unprotected_files
from genie.libs.sdk.apis.nxos.utils import free_up_disk_space


class TestFreeUpDiskSpace(TestCase):

    def test_entries_without_permissions_use_name_suffix(self):
        device = MagicMock(spec=['api', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.return_value = 120
        device.api.get_running_image.return_value = []
        device.parse.return_value = {
            'disk_used_space': '1000',
            'disk_free_space': '100',
            'disk_total_space': '1100',
            'dir': 'bootflash:/',
            'files': {
                'old-image.bin': {
                    'size': '2048',
                    'date': 'Jul 10 2026',
                    'time': '10:00:00',
                },
                'diagnostics/': {
                    'size': '4096',
                    'date': 'Jul 10 2026',
                    'time': '10:01:00',
                },
            },
        }

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertTrue(result)
        device.api.delete_unprotected_files.assert_called_once_with(
            directory='bootflash:/',
            protected=ANY,
            files_to_delete=['old-image.bin'],
            dir_output='dir output',
            allow_failure=False,
            destination='bootflash:/',
            deadline=ANY,
        )

    def test_malformed_entry_still_fails_closed(self):
        device = MagicMock(spec=['api', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.parse.return_value = {
            'disk_used_space': '1000',
            'disk_free_space': '100',
            'disk_total_space': '1100',
            'dir': 'bootflash:/',
            'files': {'malformed': None},
        }

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.api.delete_unprotected_files.assert_not_called()

    def test_explicit_symlink_type_still_fails_closed(self):
        device = MagicMock(spec=['api', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.parse.return_value = {
            'disk_used_space': '1000',
            'disk_free_space': '100',
            'disk_total_space': '1100',
            'dir': 'bootflash:/',
            'files': {
                'latest': {
                    'size': '12',
                    'permissions': 'lrwxrwxrwx',
                },
            },
        }

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.api.delete_unprotected_files.assert_not_called()

    def test_recursive_option_does_not_select_directory(self):
        device = MagicMock(spec=['api', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.return_value = 105
        device.api.get_running_image.return_value = []
        device.parse.return_value = {
            'disk_used_space': '1000',
            'disk_free_space': '100',
            'disk_total_space': '1100',
            'dir': 'bootflash:/',
            'files': {
                'old-image.bin': {
                    'size': '2048',
                    'date': 'Jul 10 2026',
                    'time': '10:00:00',
                },
                'diagnostics/': {
                    'size': '4096',
                    'date': 'Jul 10 2026',
                    'time': '10:01:00',
                },
            },
        }

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
            recursive=True,
        )

        self.assertFalse(result)
        device.api.delete_unprotected_files.assert_called_once_with(
            directory='bootflash:/',
            protected=ANY,
            files_to_delete=['old-image.bin'],
            dir_output='dir output',
            allow_failure=False,
            destination='bootflash:/',
            deadline=ANY,
        )

    def test_deletion_timeout_is_limited_by_cleanup_deadline(self):
        device = MagicMock(spec=['parse'])
        device.parse.return_value = {
            'files': {
                'old-image.bin': {'size': '2048'},
                'old-package.bin': {'size': '1024'},
            },
        }

        with patch(
                'genie.libs.sdk.apis.nxos.platform.execute.time.monotonic',
                return_value=100.0), patch(
                    'genie.libs.sdk.apis.nxos.platform.execute.FileUtils.from_device') as from_device:
            delete_unprotected_files(
                device,
                directory='bootflash:/',
                protected=[],
                files_to_delete=['old-image.bin', 'old-package.bin'],
                dir_output='dir output',
                deadline=105.0,
            )

        from_device.return_value.deletefile.assert_has_calls([
            call('bootflash:/old-image.bin', device=device, timeout_seconds=6),
            call('bootflash:/old-package.bin', device=device, timeout_seconds=6),
        ])

    def test_deletion_stops_at_cleanup_deadline(self):
        device = MagicMock(spec=['parse'])
        device.parse.return_value = {
            'files': {'old-image.bin': {'size': '2048'}},
        }

        with patch(
                'genie.libs.sdk.apis.nxos.platform.execute.time.monotonic',
                return_value=105.0), patch(
                    'genie.libs.sdk.apis.nxos.platform.execute.FileUtils.from_device') as from_device:
            result = delete_unprotected_files(
                device,
                directory='bootflash:/',
                protected=[],
                files_to_delete=['old-image.bin'],
                dir_output='dir output',
                deadline=105.0,
            )

        self.assertTrue(result)
        from_device.return_value.deletefile.assert_not_called()
