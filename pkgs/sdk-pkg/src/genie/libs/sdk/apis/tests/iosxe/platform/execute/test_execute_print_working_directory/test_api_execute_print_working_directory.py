from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.execute import execute_print_working_directory
from unicon.core.errors import SubCommandFailure


class TestExecutePrintWorkingDirectory(TestCase):

    def test_execute_print_working_directory(self):
        self.device = Mock()
        self.device.execute.return_value = 'bootflash:/'
        result = execute_print_working_directory(self.device)
        self.device.execute.assert_called_once_with('pwd')
        self.assertEqual(result, 'bootflash:/')

    def test_execute_print_working_directory_subcommandfailure(self):
        self.device = Mock()
        self.device.name = 'DeviceA'
        self.device.execute.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure) as ctx:
            execute_print_working_directory(self.device)
        self.assertIn(
            'Failed to execute pwd on device DeviceA',
            str(ctx.exception)
        )
