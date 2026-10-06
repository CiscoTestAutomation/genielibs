from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from genie.libs.sdk.apis.execute import (
    DISK_CLEANUP_PROTECTED_FILES,
    _DiskCleanupCandidate,
    _build_disk_cleanup_candidates,
    _free_up_disk_space_with_strategy,
    _run_disk_cleanup,
    free_up_disk_space as generic_free_up_disk_space,
)
from genie.libs.sdk.apis.iosxe.platform.get import (
    get_available_space_after_cleanup,
)
from genie.libs.sdk.apis.iosxe.utils import (
    _IOSXE_DISK_CLEANUP_STRATEGY,
    free_up_disk_space,
)


def parsed_directory(files, destination='bootflash:/'):
    return {
        'dir': {
            'dir': destination,
            destination: {
                'bytes_free': '100',
                'bytes_total': '1000',
                'files': files,
            },
        },
    }


class TestFreeUpDiskSpace(TestCase):

    def test_initial_output_is_reused_and_files_are_deleted_in_one_batch(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.side_effect = (
            lambda directory: get_available_space_after_cleanup(
                device, directory)
        )
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.execute.return_value = 'show file systems output'
        device.parse.side_effect = [
            parsed_directory({
                'small.log': {'permissions': '-rw-', 'size': '10'},
                'large.log': {'permissions': '-rw-', 'size': '30'},
                'medium.log': {'permissions': '-rw-', 'size': '20'},
            }),
            {
                'file_systems': {
                    1: {
                        'free_size': 200,
                        'prefixes': 'flash: bootflash:',
                    },
                },
            },
        ]

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=150,
            skip_deletion=False,
            protected_files=[],
            dir_output='captured dir output',
        )

        self.assertTrue(result)
        device.execute.assert_called_once_with(
            'show file systems', timeout=30)
        device.parse.assert_has_calls([
            call('dir bootflash:/', output='captured dir output'),
            call('show file systems', output='show file systems output'),
        ])
        device.api.get_available_space.assert_called_once_with(
            directory='bootflash:/', output='captured dir output')
        device.api.get_available_space_after_cleanup.assert_called_once_with(
            directory='bootflash:/')
        deletion = device.api.delete_unprotected_files.call_args
        self.assertEqual(
            deletion.kwargs['files_to_delete'],
            ['large.log', 'medium.log', 'small.log'])
        self.assertEqual(device.api.delete_unprotected_files.call_count, 1)
        device.api.verify_enough_disk_space.assert_not_called()

    def test_unknown_initial_space_never_deletes(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = None

        result = generic_free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='truncated dir output',
        )

        self.assertFalse(result)
        device.parse.assert_not_called()
        device.api.get_running_image.assert_not_called()
        device.api.delete_unprotected_files.assert_not_called()

    def test_protected_running_package_and_configuration_files_are_safe(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.return_value = 200
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.parse.return_value = parsed_directory({
            'running.bin': {'permissions': '-rw-', 'size': '900'},
            'incoming.bin': {'permissions': '-rw-', 'size': '800'},
            'packages.conf': {'permissions': '-rw-', 'size': '700'},
            'rpboot.pkg': {'permissions': '-rw-', 'size': '600'},
            'config.text': {'permissions': '-rw-', 'size': '500'},
            '.installer': {'permissions': 'drwx', 'size': '400'},
            'old.log': {'permissions': '-rw-', 'size': '100'},
        })

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=150,
            skip_deletion=False,
            protected_files=['incoming.bin', 'rpboot.pkg'],
            dir_output='dir output',
        )

        self.assertTrue(result)
        deletion = device.api.delete_unprotected_files.call_args
        self.assertEqual(deletion.kwargs['files_to_delete'], ['old.log'])
        protected = deletion.kwargs['protected']
        self.assertIn('running.bin', protected)
        self.assertIn('incoming.bin', protected)
        self.assertIn('rpboot.pkg', protected)
        self.assertTrue(DISK_CLEANUP_PROTECTED_FILES.issubset(protected))

    def test_running_image_without_path_separator_is_protected(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.return_value = 200
        device.api.get_running_image.return_value = 'bootflash:running.bin'
        device.parse.return_value = parsed_directory({
            'running.bin': {'permissions': '-rw-', 'size': '900'},
            'old.log': {'permissions': '-rw-', 'size': '100'},
        })

        result = generic_free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertTrue(result)
        deletion = device.api.delete_unprotected_files.call_args
        self.assertEqual(deletion.kwargs['files_to_delete'], ['old.log'])
        self.assertIn('running.bin', deletion.kwargs['protected'])

    def test_non_parenthesized_regex_protects_matching_file(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.return_value = 200
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.parse.return_value = parsed_directory({
            'foo.bin': {'permissions': '-rw-', 'size': '100'},
        })

        result = generic_free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[r'foo(\.bin)?'],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.parse.assert_called_once_with(
            'dir bootflash:/', output='dir output')
        device.api.delete_unprotected_files.assert_not_called()
        device.api.get_available_space_after_cleanup.assert_not_called()

    def test_non_recursive_iosxe_cleanup_passes_deadline(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.return_value = 200
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.parse.return_value = parsed_directory({
            'old.log': {'permissions': '-rw-', 'size': '100'},
        })

        result = _free_up_disk_space_with_strategy(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
            recursive=False,
            cleanup_strategy=_IOSXE_DISK_CLEANUP_STRATEGY,
        )

        self.assertTrue(result)
        deletion = device.api.delete_unprotected_files.call_args
        self.assertIn('deadline', deletion.kwargs)
        self.assertNotIn('recursive', deletion.kwargs)

    def test_permission_type_keeps_directory_out_of_file_batch(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.side_effect = [105, 120]
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.parse.return_value = parsed_directory({
            'core': {'permissions': 'drwx', 'size': '9000'},
            'old.log': {'permissions': '-rw-', 'size': '100'},
        })

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertTrue(result)
        calls = device.api.delete_unprotected_files.call_args_list
        self.assertEqual(calls[0].kwargs['files_to_delete'], ['old.log'])
        self.assertNotIn('recursive', calls[0].kwargs)
        self.assertEqual(calls[1].kwargs['files_to_delete'], ['core'])
        self.assertTrue(calls[1].kwargs['recursive'])
        self.assertIn('timeout', calls[1].kwargs)

    def test_unknown_entry_type_is_not_a_cleanup_candidate(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.return_value = 200
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.parse.return_value = parsed_directory({
            'unknown-entry': {'permissions': '', 'size': '9000'},
            'old.log': {'permissions': '-rw-', 'size': '100'},
        })

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertTrue(result)
        self.assertEqual(
            device.api.delete_unprotected_files.call_args.kwargs[
                'files_to_delete'],
            ['old.log'],
        )

    def test_unknown_entry_size_is_not_a_cleanup_candidate(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.parse.return_value = parsed_directory({
            'old.log': {'permissions': '-rw-', 'size': 'unknown'},
        })

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

    def test_boolean_entry_size_is_not_a_cleanup_candidate(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.parse.return_value = parsed_directory({
            'old.log': {'permissions': '-rw-', 'size': True},
        })

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.parse.assert_called_once_with(
            'dir bootflash:/', output='dir output')
        device.api.delete_unprotected_files.assert_not_called()

    def test_malformed_candidate_tuple_is_skipped(self):
        candidates = _build_disk_cleanup_candidates([
            None,
            ('missing-type.log', 100),
            ('invalid-type.log', 100, 'file'),
            ('invalid-size.log', 'unknown', False),
            ('boolean-size.log', True, False),
        ])

        self.assertEqual(candidates, [])

    def test_unknown_post_delete_space_stops_before_another_batch(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_available_space_after_cleanup.return_value = None
        device.api.get_running_image.return_value = 'bootflash:/running.bin'
        device.parse.return_value = parsed_directory({
            'file-{:02}.log'.format(index): {
                'permissions': '-rw-', 'size': str(index),
            }
            for index in range(11)
        })

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=1000,
            skip_deletion=False,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        self.assertEqual(device.api.delete_unprotected_files.call_count, 1)
        self.assertEqual(
            len(device.api.delete_unprotected_files.call_args.kwargs[
                'files_to_delete']),
            10)

    def test_skip_deletion_returns_false_without_candidate_scan(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=True,
            protected_files=[],
            dir_output='dir output',
        )

        self.assertFalse(result)
        device.parse.assert_not_called()
        device.api.delete_unprotected_files.assert_not_called()

    def test_cleanup_deadline_stops_before_deletion(self):
        candidate = _DiskCleanupCandidate('old.log', 10, False, False)
        delete_batch = MagicMock()

        with patch(
                'genie.libs.sdk.apis.execute.time.monotonic',
                side_effect=[10, 11]):
            result = _run_disk_cleanup(
                [candidate],
                required_size=100,
                delete_batch=delete_batch,
                get_available_space=MagicMock(),
                cleanup_timeout=1,
            )

        self.assertFalse(result)
        delete_batch.assert_not_called()

    def test_candidate_limit_is_enforced(self):
        candidates = [
            _DiskCleanupCandidate(
                'file-{}.log'.format(index), 10, False, False)
            for index in range(3)
        ]
        deleted = []

        result = _run_disk_cleanup(
            candidates,
            required_size=100,
            delete_batch=lambda batch, _deadline: deleted.extend(batch),
            get_available_space=lambda: 0,
            batch_size=10,
            max_candidates=2,
            cleanup_timeout=60,
        )

        self.assertFalse(result)
        self.assertEqual([candidate.path for candidate in deleted],
                         ['file-0.log', 'file-1.log'])
