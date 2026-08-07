from unittest import TestCase
from unittest.mock import ANY, MagicMock, call, patch

from genie.libs.sdk.apis.execute import (
    _get_sorted_directory_entries,
    free_up_disk_space as generic_free_up_disk_space,
)
from genie.libs.sdk.apis.iosxe.platform.execute import delete_unprotected_files
from genie.libs.sdk.apis.iosxe.utils import free_up_disk_space


class TestFreeUpDiskSpace(TestCase):

    def test_sorted_directory_entries_orders_by_size_then_name(self):
        parsed_dir_output = {
            'dir': {
                'dir': 'bootflash:/',
                'bootflash:/': {
                    'files': {
                        'small-b': {
                            'permissions': 'drwx',
                            'size': '4096',
                        },
                        'old.log': {
                            'permissions': '-rw-',
                            'size': '8192',
                        },
                        'big': {
                            'permissions': 'drwx',
                            'size': '8192',
                        },
                        'small-a': {
                            'permissions': 'drwx',
                            'size': '4096',
                        },
                    },
                },
            },
        }

        self.assertEqual(
            _get_sorted_directory_entries(parsed_dir_output),
            ['big', 'small-a', 'small-b'])

    def test_missing_file_size_defaults_to_zero(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.api.verify_enough_disk_space.side_effect = [False, True]
        device.parse.return_value = {
            'dir': {
                'dir': 'bootflash:/',
                'bootflash:/': {
                    'files': {
                        'unknown-size.log': {
                            'permissions': None,
                            'size': None,
                        },
                    },
                },
            },
        }

        result = generic_free_up_disk_space(
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
            protected=set(),
            files_to_delete=['unknown-size.log'],
            dir_output='dir output',
            allow_failure=False,
            destination='bootflash:/',
        )

    def test_non_recursive_cleanup_filters_directory_entries(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.api.verify_enough_disk_space.side_effect = [False, True]
        device.parse.return_value = {
            'dir': {
                'dir': 'bootflash:/',
                'bootflash:/': {
                    'files': {
                        'old-image.bin': {
                            'permissions': '-rw-',
                            'size': '1024',
                        },
                        'core': {
                            'permissions': 'drwx',
                            'size': '4096',
                        },
                    },
                },
            },
        }

        result = generic_free_up_disk_space(
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
            protected=set(),
            files_to_delete=['old-image.bin'],
            dir_output='dir output',
            allow_failure=False,
            destination='bootflash:/',
        )

    def test_recursive_cleanup_deletes_directories_before_files(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.api.verify_enough_disk_space.side_effect = [
            False, False, False, True]
        device.parse.return_value = {
            'dir': {
                'dir': 'bootflash:/',
                'bootflash:/': {
                    'files': {
                        'old-image.bin': {
                            'permissions': '-rw-',
                            'size': '4096',
                        },
                        'core': {
                            'permissions': 'drwx',
                            'size': '2048',
                        },
                        'crashinfo/': {
                            'size': '4096',
                        },
                    },
                },
            },
        }

        result = free_up_disk_space(
            device,
            destination='bootflash:/',
            required_size=110,
            skip_deletion=False,
            protected_files=['image.bin'],
            dir_output='dir output',
        )

        self.assertTrue(result)
        device.api.delete_unprotected_files.assert_has_calls([
            call(
                directory='bootflash:/',
                protected={'image.bin'},
                files_to_delete=['crashinfo/'],
                dir_output='dir output',
                allow_failure=False,
                destination='bootflash:/',
                recursive=True,
                stop_check=ANY,
            ),
            call(
                directory='bootflash:/',
                protected={'image.bin'},
                files_to_delete=['core'],
                dir_output='dir output',
                allow_failure=False,
                destination='bootflash:/',
                recursive=True,
                stop_check=ANY,
            ),
            call(
                directory='bootflash:/',
                protected={'image.bin'},
                files_to_delete=['old-image.bin'],
                dir_output='dir output',
                allow_failure=False,
                destination='bootflash:/',
            ),
        ])
        self.assertEqual(device.api.delete_unprotected_files.call_count, 3)

    def test_recursive_cleanup_stops_after_directory_frees_space(self):
        device = MagicMock(spec=['api', 'execute', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.api.verify_enough_disk_space.side_effect = [
            False, True, True]
        device.parse.side_effect = [
            {
                'dir': {
                    'dir': 'bootflash:/',
                    'bootflash:/': {
                        'files': {
                            'old-image.bin': {
                                'permissions': '-rw-',
                                'size': '4096',
                            },
                            'core': {
                                'permissions': 'drwx',
                                'size': '2048',
                            },
                        },
                    },
                },
            },
            {
                'dir': {
                    'dir': 'bootflash:/',
                    'bootflash:/': {
                        'files': {
                            'core': {
                                'permissions': 'drwx',
                                'size': '2048',
                            },
                        },
                    },
                },
            },
            {
                'dir': {
                    'dir': 'bootflash:/core/',
                    'bootflash:/core/': {
                        'files': {
                            'first.log': {
                                'permissions': '-rw-',
                                'size': '1024',
                            },
                            'second.log': {
                                'permissions': '-rw-',
                                'size': '2048',
                            },
                        },
                    },
                },
            },
        ]
        file_utils = MagicMock()

        def delete_files(*args, **kwargs):
            return delete_unprotected_files(device, *args, **kwargs)

        device.api.delete_unprotected_files.side_effect = delete_files

        with patch(
            'genie.libs.sdk.apis.iosxe.platform.execute.FileUtils.from_device',
            return_value=file_utils,
        ):
            result = free_up_disk_space(
                device,
                destination='bootflash:/',
                required_size=110,
                skip_deletion=False,
                protected_files=[],
                dir_output='dir output',
            )

        self.assertTrue(result)
        file_utils.deletefile.assert_called_once_with(
            'bootflash:/core/second.log', force=True, device=device)
