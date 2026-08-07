from unittest import TestCase
from unittest.mock import MagicMock

from genie.libs.sdk.apis.execute import free_up_disk_space


class TestFreeUpDiskSpace(TestCase):

    def test_generic_cleanup_supports_dir_files_parser_shape(self):
        device = MagicMock(spec=['api', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.api.verify_enough_disk_space.side_effect = [False, True]
        device.parse.return_value = {
            'dir': {
                'dir_name': 'harddisk:',
                'total_bytes': '1000',
                'total_free_bytes': '100',
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

        self.assertTrue(result)
        device.api.delete_unprotected_files.assert_called_once_with(
            directory='harddisk:',
            protected=set(),
            files_to_delete=['old-package.pie'],
            dir_output='dir output',
            allow_failure=False,
            destination='harddisk:',
        )
