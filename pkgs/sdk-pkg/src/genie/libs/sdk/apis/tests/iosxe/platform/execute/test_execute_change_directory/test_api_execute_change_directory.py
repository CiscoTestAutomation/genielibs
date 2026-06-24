from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.execute import execute_change_directory
from unicon.core.errors import SubCommandFailure


class TestExecuteChangeDirectory(TestCase):

    def test_execute_change_directory_root(self):
        self.device = Mock()
        self.device.execute.return_value = ''
        result = execute_change_directory(self.device)
        self.device.execute.assert_called_once_with('cd')
        self.assertEqual(result, '')

    def test_execute_change_directory_file_system(self):
        self.device = Mock()
        self.device.execute.return_value = ''
        result = execute_change_directory(self.device, directory='bootflash:')
        self.device.execute.assert_called_once_with('cd bootflash:')
        self.assertEqual(result, '')

    def test_execute_change_directory_subdirectory(self):
        self.device = Mock()
        self.device.execute.return_value = ''
        result = execute_change_directory(self.device, directory='bootflash:dir1')
        self.device.execute.assert_called_once_with('cd bootflash:dir1')
        self.assertEqual(result, '')

    def test_execute_change_directory_subcommandfailure(self):
        self.device = Mock()
        self.device.name = 'DeviceA'
        self.device.execute.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure) as ctx:
            execute_change_directory(self.device, directory='bootflash:')
        self.assertIn(
            'Failed to execute cd bootflash: on device DeviceA',
            str(ctx.exception)
        )
