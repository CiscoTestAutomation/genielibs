from unittest import TestCase
from unittest.mock import ANY, MagicMock, call, patch

from genie.libs.sdk.apis.iosxe.platform.execute import (
    _get_child_directory,
    delete_unprotected_files,
)


class TestDeleteUnprotectedFiles(TestCase):

    def test_get_child_directory_normalizes_separator(self):
        self.assertEqual(
            _get_child_directory('bootflash:', 'core'),
            'bootflash:/core/')
        self.assertEqual(
            _get_child_directory('bootflash:/', 'core'),
            'bootflash:/core/')
        self.assertEqual(
            _get_child_directory('bootflash:/core', 'modules/'),
            'bootflash:/core/modules/')

    def test_non_recursive_deletion_skips_directory(self):
        device = MagicMock()
        device.parse.return_value = {
            'dir': {
                'dir': 'bootflash:/',
                'bootflash:/': {
                    'files': {
                        'core': {
                            'permissions': 'drwx',
                            'size': '4096',
                        },
                        'old-crashinfo.log': {
                            'permissions': '-rw-',
                            'size': '1024',
                        },
                    },
                },
            },
        }
        file_utils = MagicMock()

        with patch(
            'genie.libs.sdk.apis.iosxe.platform.execute.FileUtils.from_device',
            return_value=file_utils,
        ):
            delete_unprotected_files(
                device,
                directory='bootflash:/',
                protected=[],
                destination='bootflash:/',
            )

        file_utils.deletefile.assert_called_once_with(
            'bootflash:/old-crashinfo.log', force=True, device=device)

    def test_recursive_deletion_traverses_directory(self):
        device = MagicMock()
        device.parse.side_effect = [
            {
                'dir': {
                    'dir': 'bootflash:/',
                    'bootflash:/': {
                        'files': {
                            'core': {
                                'permissions': 'drwx',
                                'size': '4096',
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
                            'crashinfo.log': {
                                'permissions': '-rw-',
                                'size': '1024',
                            },
                            'nested': {
                                'permissions': 'drwx',
                                'size': '512',
                            },
                        },
                    },
                },
            },
            {
                'dir': {
                    'dir': 'bootflash:/core/nested/',
                    'bootflash:/core/nested/': {
                        'files': {
                            'nested-crashinfo.log': {
                                'permissions': '-rw-',
                                'size': '512',
                            },
                        },
                    },
                },
            },
        ]
        file_utils = MagicMock()

        with patch(
            'genie.libs.sdk.apis.iosxe.platform.execute.FileUtils.from_device',
            return_value=file_utils,
        ):
            delete_unprotected_files(
                device,
                directory='bootflash:/',
                protected=[],
                files_to_delete=['core'],
                dir_output='root dir output',
                destination='bootflash:/',
                recursive=True,
            )

        device.parse.assert_has_calls([
            call('dir bootflash:/', output='root dir output'),
            call('dir bootflash:/core/', output=ANY),
            call('dir bootflash:/core/nested/', output=ANY),
        ])
        device.execute.assert_has_calls([
            call('dir bootflash:/core/', timeout=300),
            call('dir bootflash:/core/nested/', timeout=300),
        ])
        file_utils.deletefile.assert_has_calls([
            call(
                'bootflash:/core/nested/nested-crashinfo.log',
                force=True,
                device=device),
            call('bootflash:/core/crashinfo.log', force=True, device=device),
        ])
        self.assertEqual(file_utils.deletefile.call_count, 2)

    def test_recursive_deletion_normalizes_filesystem_root_path(self):
        device = MagicMock()
        device.parse.side_effect = [
            {
                'dir': {
                    'dir': 'bootflash:',
                    'bootflash:': {
                        'files': {
                            'core': {
                                'permissions': 'drwx',
                                'size': '4096',
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
                            'big.core.gz': {
                                'permissions': '-rw-',
                                'size': '900',
                            },
                            'modules': {
                                'permissions': 'drwx',
                                'size': '100',
                            },
                        },
                    },
                },
            },
            {
                'dir': {
                    'dir': 'bootflash:/core/modules/',
                    'bootflash:/core/modules/': {
                        'files': {
                            'module.log': {
                                'permissions': '-rw-',
                                'size': '100',
                            },
                        },
                    },
                },
            },
        ]
        file_utils = MagicMock()

        with patch(
            'genie.libs.sdk.apis.iosxe.platform.execute.FileUtils.from_device',
            return_value=file_utils,
        ):
            delete_unprotected_files(
                device,
                directory='bootflash:',
                protected=[],
                files_to_delete=['core'],
                destination='bootflash:',
                recursive=True,
            )

        device.parse.assert_has_calls([
            call('dir bootflash:', output=ANY),
            call('dir bootflash:/core/', output=ANY),
            call('dir bootflash:/core/modules/', output=ANY),
        ])
        device.execute.assert_has_calls([
            call('dir bootflash:', timeout=300),
            call('dir bootflash:/core/', timeout=300),
            call('dir bootflash:/core/modules/', timeout=300),
        ])
        file_utils.deletefile.assert_has_calls([
            call(
                'bootflash:/core/modules/module.log',
                force=True,
                device=device),
            call('bootflash:/core/big.core.gz', force=True, device=device),
        ])
        self.assertEqual(file_utils.deletefile.call_count, 2)

    def test_recursive_deletion_preserves_protected_files(self):
        device = MagicMock()
        device.parse.side_effect = [
            {
                'dir': {
                    'dir': 'bootflash:/',
                    'bootflash:/': {
                        'files': {
                            'core': {
                                'permissions': 'drwx',
                                'size': '4096',
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
                            'keep.log': {
                                'permissions': '-rw-',
                                'size': '1024',
                            },
                            'delete.log': {
                                'permissions': '-rw-',
                                'size': '1024',
                            },
                        },
                    },
                },
            },
        ]
        file_utils = MagicMock()

        with patch(
            'genie.libs.sdk.apis.iosxe.platform.execute.FileUtils.from_device',
            return_value=file_utils,
        ):
            delete_unprotected_files(
                device,
                directory='bootflash:/',
                protected=['keep.log'],
                files_to_delete=['core'],
                destination='bootflash:/',
                recursive=True,
            )

        file_utils.deletefile.assert_called_once_with(
            'bootflash:/core/delete.log', force=True, device=device)

    def test_recursive_deletion_stops_when_stop_check_succeeds(self):
        device = MagicMock()
        device.parse.side_effect = [
            {
                'dir': {
                    'dir': 'bootflash:/',
                    'bootflash:/': {
                        'files': {
                            'core': {
                                'permissions': 'drwx',
                                'size': '4096',
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
        stop_check = MagicMock(return_value=True)

        with patch(
            'genie.libs.sdk.apis.iosxe.platform.execute.FileUtils.from_device',
            return_value=file_utils,
        ):
            result = delete_unprotected_files(
                device,
                directory='bootflash:/',
                protected=[],
                files_to_delete=['core'],
                destination='bootflash:/',
                recursive=True,
                stop_check=stop_check,
            )

        self.assertTrue(result)
        file_utils.deletefile.assert_called_once_with(
            'bootflash:/core/second.log', force=True, device=device)
        stop_check.assert_called_once()
