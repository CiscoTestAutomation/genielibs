from unittest import TestCase
from unittest.mock import ANY, MagicMock, patch

from genie.libs.sdk.apis.apic.platform.utils import (
    delete_unprotected_files,
    free_up_disk_space,
)


class TestApicFreeUpDiskSpace(TestCase):

    def test_deletion_uses_filtered_regular_file_candidates(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.parse.side_effect = [
            {
                'directory': {
                    '/data': {
                        'available': 100,
                        'total': 1000,
                        'use_percentage': 90,
                    },
                },
            },
            {
                'files': {
                    'protected.iso': {'mode': '-rw-r--r--', 'size': 900},
                    'directory-without-slash': {
                        'mode': 'drwxr-xr-x', 'size': 800,
                    },
                    'symlink': {'mode': 'lrwxrwxrwx', 'size': 700},
                    'large.log': {'mode': '-rw-r--r--', 'size': 600},
                    'small.log': {'mode': '-rw-r--r--', 'size': 500},
                },
            },
        ]
        device.execute.return_value = 'captured ls output'
        device.api.get_available_space.return_value = 200

        result = free_up_disk_space(
            device,
            destination='/data',
            required_size=150,
            skip_deletion=False,
            protected_files=['protected.iso'],
            dir_output='captured df output',
        )

        self.assertTrue(result)
        device.api.delete_unprotected_files.assert_called_once_with(
            directory='/data',
            protected=['protected.iso'],
            files_to_delete=['large.log', 'small.log'],
            dir_output='captured ls output',
            deadline=ANY,
        )
        device.api.verify_enough_disk_space.assert_not_called()

    def test_unknown_initial_space_does_not_delete(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.parse.return_value = {'directory': {'/data': {}}}

        result = free_up_disk_space(
            device,
            destination='/data',
            required_size=150,
            skip_deletion=False,
            protected_files=[],
            dir_output='malformed df output',
        )

        self.assertFalse(result)
        device.execute.assert_not_called()
        device.api.delete_unprotected_files.assert_not_called()

    def test_apic_regex_filtering_controls_the_actual_batch(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.parse.side_effect = [
            {
                'directory': {
                    '/data': {
                        'available': 100,
                        'total': 1000,
                        'use_percentage': 90,
                    },
                },
            },
            {
                'files': {
                    'keep.log': {'mode': '-rw-r--r--', 'size': 900},
                    'delete.iso': {'mode': '-rw-r--r--', 'size': 500},
                },
            },
        ]
        device.execute.return_value = 'captured ls output'
        device.api.get_available_space.return_value = 200
        apic_clean_protection = [r'^.+$(?<!\.bin)(?<!\.iso)']

        result = free_up_disk_space(
            device,
            destination='/data',
            required_size=150,
            skip_deletion=False,
            protected_files=apic_clean_protection,
            dir_output='captured df output',
        )

        self.assertTrue(result)
        device.api.delete_unprotected_files.assert_called_once_with(
            directory='/data',
            protected=apic_clean_protection,
            files_to_delete=['delete.iso'],
            dir_output='captured ls output',
            deadline=ANY,
        )

    def test_skip_deletion_does_not_list_candidates(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.parse.return_value = {
            'directory': {
                '/data': {
                    'available': 100,
                    'total': 1000,
                    'use_percentage': 90,
                },
            },
        }

        result = free_up_disk_space(
            device,
            destination='/data',
            required_size=150,
            skip_deletion=True,
            protected_files=[],
            dir_output='captured df output',
        )

        self.assertFalse(result)
        device.execute.assert_not_called()
        device.api.delete_unprotected_files.assert_not_called()

    def test_delete_api_never_sends_directory_or_symlink_to_fileutils(self):
        device = MagicMock()
        device.parse.return_value = {
            'files': {
                'regular.log': {'mode': '-rw-r--r--', 'size': 100},
                'directory-without-slash': {
                    'mode': 'drwxr-xr-x', 'size': 100,
                },
                'symlink': {'mode': 'lrwxrwxrwx', 'size': 100},
            },
        }
        file_utils = MagicMock()

        with patch(
                'genie.libs.sdk.apis.apic.platform.utils.'
                'FileUtils.from_device',
                return_value=file_utils):
            delete_unprotected_files(
                device,
                directory='/data',
                protected=[],
                files_to_delete=[
                    'directory-without-slash', 'symlink', 'regular.log'],
                dir_output='captured ls output',
            )

        file_utils.deletefile.assert_called_once_with(
            'regular.log', timeout_seconds=300, device=device)

    def test_delete_api_malformed_listing_does_not_delete(self):
        device = MagicMock()
        device.parse.return_value = {'files': ['malformed']}
        file_utils = MagicMock()

        with patch(
                'genie.libs.sdk.apis.apic.platform.utils.'
                'FileUtils.from_device',
                return_value=file_utils):
            delete_unprotected_files(
                device,
                directory='/data',
                protected=[],
                files_to_delete=['malformed'],
                dir_output='captured ls output',
            )

        file_utils.deletefile.assert_not_called()

    def test_delete_api_malformed_file_details_do_not_delete(self):
        device = MagicMock()
        device.parse.return_value = {
            'files': {
                'malformed': ['not', 'file', 'details'],
            },
        }
        file_utils = MagicMock()

        with patch(
                'genie.libs.sdk.apis.apic.platform.utils.'
                'FileUtils.from_device',
                return_value=file_utils) as from_device:
            result = delete_unprotected_files(
                device,
                directory='/data',
                protected=[],
                files_to_delete=['malformed'],
                dir_output='captured ls output',
            )

        self.assertIsNone(result)
        from_device.assert_not_called()
        file_utils.deletefile.assert_not_called()

    def test_delete_api_parser_failure_does_not_delete(self):
        device = MagicMock()
        device.parse.side_effect = ValueError('malformed parser output')
        file_utils = MagicMock()

        with patch(
                'genie.libs.sdk.apis.apic.platform.utils.'
                'FileUtils.from_device',
                return_value=file_utils) as from_device:
            result = delete_unprotected_files(
                device,
                directory='/data',
                protected=[],
                files_to_delete=['unsafe.log'],
                dir_output='captured ls output',
            )

        self.assertIsNone(result)
        from_device.assert_not_called()
        file_utils.deletefile.assert_not_called()

    def test_unknown_file_size_is_not_a_cleanup_candidate(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.parse.side_effect = [
            {
                'directory': {
                    '/data': {
                        'available': 100,
                        'total': 1000,
                        'use_percentage': 90,
                    },
                },
            },
            {
                'files': {
                    'old.log': {
                        'mode': '-rw-r--r--',
                        'size': 'unknown',
                    },
                },
            },
        ]
        device.execute.return_value = 'captured ls output'

        result = free_up_disk_space(
            device,
            destination='/data',
            required_size=150,
            skip_deletion=False,
            protected_files=[],
            dir_output='captured df output',
        )

        self.assertFalse(result)
        device.api.delete_unprotected_files.assert_not_called()

    def test_boolean_file_size_is_not_a_cleanup_candidate(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.parse.side_effect = [
            {
                'directory': {
                    '/data': {
                        'available': 100,
                        'total': 1000,
                        'use_percentage': 90,
                    },
                },
            },
            {
                'files': {
                    'old.log': {
                        'mode': '-rw-r--r--',
                        'size': True,
                    },
                },
            },
        ]
        device.execute.return_value = 'captured ls output'

        result = free_up_disk_space(
            device,
            destination='/data',
            required_size=150,
            skip_deletion=False,
            protected_files=[],
            dir_output='captured df output',
        )

        self.assertFalse(result)
        device.execute.assert_called_once_with('ls -l /data')
        device.api.delete_unprotected_files.assert_not_called()
