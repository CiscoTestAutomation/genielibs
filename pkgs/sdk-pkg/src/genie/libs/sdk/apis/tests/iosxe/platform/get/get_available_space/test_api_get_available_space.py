from unittest import TestCase
from unittest.mock import MagicMock, call

from genie.libs.sdk.apis.iosxe.platform.get import (
    get_available_space,
    get_available_space_after_cleanup,
)


class TestGetAvailableSpace(TestCase):

    def test_captured_directory_output_is_reused(self):
        device = MagicMock()
        device.parse.return_value = {
            'dir': {
                'dir': 'bootflash:/',
                'bootflash:/': {'bytes_free': '1234'},
            },
        }

        result = get_available_space(
            device, directory='bootflash:/', output='captured dir')

        self.assertEqual(result, 1234)
        device.parse.assert_called_once_with(
            'dir bootflash:/', output='captured dir')
        device.execute.assert_not_called()

    def test_default_query_preserves_directory_listing_behavior(self):
        device = MagicMock()
        device.parse.return_value = {
            'dir': {
                'dir': 'bootflash:/',
                'bootflash:/': {'bytes_free': '1234'},
            },
        }

        result = get_available_space(device, directory='bootflash:/')

        self.assertEqual(result, 1234)
        device.parse.assert_called_once_with(
            'dir bootflash:/', output=None)
        device.execute.assert_not_called()

    def test_post_delete_check_uses_bounded_show_file_systems(self):
        device = MagicMock()
        device.execute.return_value = 'show file systems output'
        device.parse.return_value = {
            'file_systems': {
                1: {
                    'free_size': 4835155968,
                    'prefixes': 'flash: bootflash: flash-1:',
                },
                2: {
                    'free_size': 3943694336,
                    'prefixes': 'flash-2: stby-flash:',
                },
            },
        }

        result = get_available_space_after_cleanup(
            device, directory='bootflash:/images/')

        self.assertEqual(result, 4835155968)
        device.execute.assert_called_once_with(
            'show file systems', timeout=30)
        device.parse.assert_called_once_with(
            'show file systems', output='show file systems output')
        self.assertNotIn(
            call('dir bootflash:/images/'), device.execute.call_args_list)

    def test_unmatched_filesystem_is_unverified(self):
        device = MagicMock()
        device.execute.return_value = 'show file systems output'
        device.parse.return_value = {
            'file_systems': {
                1: {'free_size': 100, 'prefixes': 'flash:'},
            },
        }

        self.assertIsNone(
            get_available_space_after_cleanup(
                device, directory='usbflash0:/'))

    def test_malformed_filesystem_free_size_is_unverified(self):
        device = MagicMock()
        device.execute.return_value = 'show file systems output'
        device.parse.return_value = {
            'file_systems': {
                1: {'free_size': 'unknown', 'prefixes': 'bootflash:'},
            },
        }

        self.assertIsNone(
            get_available_space_after_cleanup(
                device, directory='bootflash:/'))

    def test_truncated_captured_directory_output_is_unverified(self):
        device = MagicMock()
        device.parse.return_value = {'dir': {'dir': 'bootflash:/'}}

        self.assertIsNone(get_available_space(
            device,
            directory='bootflash:/',
            output='truncated dir output',
        ))
        device.execute.assert_not_called()
