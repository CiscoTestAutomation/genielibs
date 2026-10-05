from unittest import TestCase
from unittest.mock import ANY, MagicMock, call, patch

from genie.libs.sdk.apis.execute import free_up_disk_space
from genie.libs.sdk.apis.iosxr.platform.execute import delete_unprotected_files
from genie.libs.sdk.apis.utils import get_available_space_after_cleanup


class TestFreeUpDiskSpace(TestCase):

    def _device_with_files(self, files):
        device = MagicMock(spec=['api', 'os', 'parse'])
        device.os = 'iosxr'
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.parse.return_value = {
            'dir': {
                'dir_name': 'harddisk:',
                'total_bytes': '1000',
                'total_free_bytes': '100',
                'files': files,
            },
        }
        return device

    def test_generic_cleanup_supports_dir_files_parser_shape(self):
        device = self._device_with_files({
            'old-package.pie': {
                'size': '2048',
                'permission': '-rw-',
            },
        })
        device.api.get_available_space.side_effect = [100, 120]
        device.api.get_available_space_after_cleanup.side_effect = (
            lambda directory: get_available_space_after_cleanup(
                device, directory)
        )

        result = free_up_disk_space(
            device,
            destination='harddisk:',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertTrue(result)
        device.api.get_available_space.assert_has_calls([
            call(directory='harddisk:', output='dir output'),
            call(directory='harddisk:'),
        ])
        device.api.delete_unprotected_files.assert_called_once_with(
            directory='harddisk:',
            protected=ANY,
            files_to_delete=['old-package.pie'],
            dir_output='dir output',
            allow_failure=False,
            destination='harddisk:',
            deadline=ANY,
        )

    def test_directory_is_not_a_cleanup_candidate(self):
        device = self._device_with_files({
            'diagnostics': {
                'size': '4096',
                'permission': 'drwxr-xr-x',
            },
        })

        result = free_up_disk_space(
            device,
            destination='harddisk:',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.api.delete_unprotected_files.assert_not_called()

    def test_recursive_cleanup_is_not_forwarded_to_unsupported_platform(self):
        device = self._device_with_files({
            'old-package.pie': {
                'size': '2048',
                'permission': '-rw-',
            },
            'diagnostics': {
                'size': '4096',
                'permission': 'drwxr-xr-x',
            },
        })
        device.api.get_available_space_after_cleanup.return_value = 120

        result = free_up_disk_space(
            device,
            destination='harddisk:',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
            recursive=True,
        )

        self.assertTrue(result)
        device.api.delete_unprotected_files.assert_called_once_with(
            directory='harddisk:',
            protected=ANY,
            files_to_delete=['old-package.pie'],
            dir_output='dir output',
            allow_failure=False,
            destination='harddisk:',
            deadline=ANY,
        )

    def test_iosxr_deletion_timeout_is_limited_by_cleanup_deadline(self):
        device = self._device_with_files({
            'old-package.pie': {
                'size': '2048',
                'permission': '-rw-',
            },
            'old-install.pie': {
                'size': '1024',
                'permission': '-rw-',
            },
        })

        with patch(
                'genie.libs.sdk.apis.iosxr.platform.execute.time.monotonic',
                return_value=100.0), patch(
                    'genie.libs.sdk.apis.iosxr.platform.execute.FileUtils.from_device') as from_device:
            delete_unprotected_files(
                device,
                directory='harddisk:',
                protected=[],
                files_to_delete=['old-package.pie', 'old-install.pie'],
                dir_output='dir output',
                destination='harddisk:',
                deadline=105.0,
            )

        from_device.return_value.deletefile.assert_has_calls([
            call('harddisk:old-package.pie', device=device, timeout_seconds=6),
            call('harddisk:old-install.pie', device=device, timeout_seconds=6),
        ])

    def test_iosxr_deletion_stops_at_cleanup_deadline(self):
        device = self._device_with_files({
            'old-package.pie': {
                'size': '2048',
                'permission': '-rw-',
            },
        })

        with patch(
                'genie.libs.sdk.apis.iosxr.platform.execute.time.monotonic',
                return_value=105.0), patch(
                    'genie.libs.sdk.apis.iosxr.platform.execute.FileUtils.from_device') as from_device:
            result = delete_unprotected_files(
                device,
                directory='harddisk:',
                protected=[],
                files_to_delete=['old-package.pie'],
                dir_output='dir output',
                destination='harddisk:',
                deadline=105.0,
            )

        self.assertTrue(result)
        from_device.return_value.deletefile.assert_not_called()

    def test_iosxr_deletion_only_deletes_verified_regular_files(self):
        device = self._device_with_files({
            'old-package.pie': {
                'size': '2048',
                'permission': '-rw-r--r--',
            },
            'diagnostics': {
                'size': '4096',
                'permission': 'drwxr-xr-x',
            },
            'latest': {
                'size': '12',
                'permission': 'lrwxrwxrwx',
            },
            'unknown': {
                'size': '1024',
            },
        })

        with patch(
                'genie.libs.sdk.apis.iosxr.platform.execute.FileUtils.from_device') as from_device:
            delete_unprotected_files(
                device,
                directory='harddisk:',
                protected=[],
                files_to_delete=[
                    'old-package.pie', 'diagnostics', 'latest', 'unknown'],
                dir_output='dir output',
                destination='harddisk:',
            )

        from_device.return_value.deletefile.assert_called_once_with(
            'harddisk:old-package.pie', device=device)

    def test_iosxr_unsafe_entries_are_never_deleted(self):
        unsafe_entries = {
            'directory': ('diagnostics', {
                'size': '4096',
                'permission': 'drwxr-xr-x',
            }),
            'symlink': ('latest', {
                'size': '12',
                'permission': 'lrwxrwxrwx',
            }),
            'unknown_type': ('unknown', {
                'size': '1024',
            }),
            'malformed_details': ('malformed', None),
        }

        for case_name, (file_name, file_details) in unsafe_entries.items():
            with self.subTest(case=case_name):
                device = self._device_with_files({file_name: file_details})
                with patch(
                        'genie.libs.sdk.apis.iosxr.platform.execute.FileUtils.from_device') as from_device:
                    result = delete_unprotected_files(
                        device,
                        directory='harddisk:',
                        protected=[],
                        files_to_delete=[file_name],
                        dir_output='dir output',
                        destination='harddisk:',
                    )

                self.assertIsNone(result)
                from_device.return_value.deletefile.assert_not_called()

    def test_iosxr_deletion_without_subset_deletes_only_safe_files(self):
        device = self._device_with_files({
            'old-package.pie': {
                'size': '2048',
                'permission': '-rw-',
            },
            'diagnostics': {
                'size': '4096',
                'permission': 'drwxr-xr-x',
            },
        })

        with patch(
                'genie.libs.sdk.apis.iosxr.platform.execute.FileUtils.from_device') as from_device:
            delete_unprotected_files(
                device,
                directory='harddisk:',
                protected=[],
                dir_output='dir output',
                destination='harddisk:',
            )

        from_device.return_value.deletefile.assert_called_once_with(
            'harddisk:old-package.pie', device=device)

    def test_iosxr_deletion_empty_subset_deletes_nothing(self):
        device = self._device_with_files({
            'old-package.pie': {
                'size': '2048',
                'permission': '-rw-',
            },
        })

        with patch(
                'genie.libs.sdk.apis.iosxr.platform.execute.FileUtils.from_device') as from_device:
            result = delete_unprotected_files(
                device,
                directory='harddisk:',
                protected=[],
                files_to_delete=[],
                dir_output='dir output',
                destination='harddisk:',
            )

        self.assertIsNone(result)
        from_device.return_value.deletefile.assert_not_called()

    def test_iosxr_deletion_protects_exact_and_regex_matches(self):
        device = self._device_with_files({
            'packages.conf': {
                'size': '2048',
                'permission': '-rw-',
            },
            'config_backup': {
                'size': '1024',
                'permission': '-rw-',
            },
        })

        with patch(
                'genie.libs.sdk.apis.iosxr.platform.execute.FileUtils.from_device') as from_device:
            result = delete_unprotected_files(
                device,
                directory='harddisk:',
                protected={'packages.conf', '(config.*)'},
                files_to_delete=['packages.conf', 'config_backup'],
                dir_output='dir output',
                destination='harddisk:',
            )

        self.assertIsNone(result)
        from_device.return_value.deletefile.assert_not_called()

    def test_iosxr_deletion_malformed_listing_fails_closed(self):
        device = MagicMock(spec=['parse'])
        device.parse.return_value = {
            'unexpected': {
                'files': {
                    'old-package.pie': {
                        'size': '2048',
                        'permission': '-rw-',
                    },
                },
            },
        }

        with patch(
                'genie.libs.sdk.apis.iosxr.platform.execute.FileUtils.from_device') as from_device:
            result = delete_unprotected_files(
                device,
                directory='harddisk:',
                protected=[],
                files_to_delete=['old-package.pie'],
                dir_output='dir output',
                destination='harddisk:',
            )

        self.assertIsNone(result)
        from_device.return_value.deletefile.assert_not_called()

    def test_symlink_is_not_a_cleanup_candidate(self):
        device = self._device_with_files({
            'latest': {
                'size': '12',
                'permission': 'lrwxrwxrwx',
            },
        })

        result = free_up_disk_space(
            device,
            destination='harddisk:',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.api.delete_unprotected_files.assert_not_called()

    def test_malformed_file_details_fail_closed(self):
        device = self._device_with_files({'malformed': None})

        result = free_up_disk_space(
            device,
            destination='harddisk:',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.api.delete_unprotected_files.assert_not_called()

    def test_unsupported_fallback_shape_fails_closed(self):
        device = MagicMock(spec=['api', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.parse.return_value = {
            'unexpected': {
                'files': {
                    'old-package.pie': {
                        'size': '2048',
                        'permission': '-rw-',
                    },
                },
            },
        }

        result = free_up_disk_space(
            device,
            destination='harddisk:',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.api.delete_unprotected_files.assert_not_called()
