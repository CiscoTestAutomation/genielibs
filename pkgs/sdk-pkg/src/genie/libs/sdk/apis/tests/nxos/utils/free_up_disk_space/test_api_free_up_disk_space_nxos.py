from unittest import TestCase
from unittest.mock import MagicMock

from genie.libs.sdk.apis.execute import free_up_disk_space


class TestFreeUpDiskSpace(TestCase):

    def test_generic_cleanup_supports_top_level_files_parser_shape(self):
        device = MagicMock(spec=['api', 'parse'])
        device.api.get_available_space.return_value = 100
        device.api.get_running_image.return_value = []
        device.api.verify_enough_disk_space.side_effect = [False, True]
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
            protected=set(),
            files_to_delete=['old-image.bin'],
            dir_output='dir output',
            allow_failure=False,
            destination='bootflash:/',
        )
