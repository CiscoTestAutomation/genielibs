from unittest import TestCase
from unittest.mock import MagicMock

from genie.libs.sdk.apis.iosxe.platform.execute import create_empty_file, touch_file


class TestCreateEmptyFile(TestCase):

    def test_create_empty_file(self):
        device = MagicMock()
        device.api.verify_file_exists.return_value = False

        create_empty_file(device, directory='bootflash:/', file_name='test.txt')

        self.assertEqual(device.execute.call_count, 2)
        device.api.verify_file_exists.assert_called_once_with(
            file='bootflash:/test.txt',
            dir_output=device.execute.return_value,
        )
        call_args = device.execute.call_args_list[1]
        self.assertEqual(call_args[0][0], 'copy null: bootflash:/test.txt')
        dialog = call_args.kwargs['reply']
        self.assertEqual(
            [statement.pattern for statement in dialog],
            [
                r'Destination filename \[.*\]\?',
            ],
        )

    def test_create_empty_file_in_subdirectory(self):
        device = MagicMock()
        device.api.verify_file_exists.return_value = False

        create_empty_file(
            device, directory='bootflash:/core', file_name='test.txt')

        self.assertEqual(device.execute.call_args_list[0][0][0],
                         'dir bootflash:/core/')
        device.api.verify_file_exists.assert_called_once_with(
            file='bootflash:/core/test.txt',
            dir_output=device.execute.return_value,
        )
        call_args = device.execute.call_args_list[1]
        self.assertEqual(
            call_args[0][0], 'copy null: bootflash:/core/test.txt')

    def test_create_empty_file_skips_existing_file(self):
        device = MagicMock()
        device.api.verify_file_exists.return_value = True

        create_empty_file(device, directory='bootflash:/', file_name='test.txt')

        device.execute.assert_called_once_with('dir bootflash:/')

    def test_create_empty_file_normalizes_colon_directory(self):
        device = MagicMock()
        device.api.verify_file_exists.return_value = True

        create_empty_file(device, directory='bootflash:', file_name='test.txt')

        device.execute.assert_called_once_with('dir bootflash:/')
        device.api.verify_file_exists.assert_called_once_with(
            file='bootflash:/test.txt',
            dir_output=device.execute.return_value,
        )

    def test_create_empty_file_normalizes_subdirectory(self):
        device = MagicMock()
        device.api.verify_file_exists.return_value = True

        create_empty_file(
            device, directory='bootflash:/core', file_name='test.txt')

        device.execute.assert_called_once_with('dir bootflash:/core/')
        device.api.verify_file_exists.assert_called_once_with(
            file='bootflash:/core/test.txt',
            dir_output=device.execute.return_value,
        )

    def test_create_empty_file_overwrites_existing_file(self):
        device = MagicMock()

        create_empty_file(
            device, directory='bootflash:/', file_name='test.txt',
            overwrite=True)

        device.api.verify_file_exists.assert_not_called()
        dialog = device.execute.call_args.kwargs['reply']
        self.assertEqual(
            [statement.pattern for statement in dialog],
            [
                r'Destination filename \[.*\]\?',
                (r'%Warning:.*existing with this name\s+Do you want to over '
                 r'write\? \[confirm\]'),
            ],
        )

    def test_touch_file_deprecated_wrapper(self):
        device = MagicMock()
        device.api.verify_file_exists.return_value = False

        self.assertEqual(
            touch_file.__deprecated__,
            "please use create_empty_file()")

        with self.assertWarnsRegex(
                FutureWarning, "please use create_empty_file"):
            touch_file(device, directory='bootflash:/', file_name='test.txt')

        device.api.verify_file_exists.assert_called_once_with(
            file='bootflash:/test.txt',
            dir_output=device.execute.return_value,
        )
        call_args = device.execute.call_args_list[1]
        self.assertEqual(call_args[0][0], 'copy null: bootflash:/test.txt')
