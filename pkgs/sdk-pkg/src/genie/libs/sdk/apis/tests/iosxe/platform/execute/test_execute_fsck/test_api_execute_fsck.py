from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.execute import execute_fsck
from unicon.core.errors import SubCommandFailure


class TestExecuteFsck(TestCase):

    def test_execute_fsck(self):
        self.device = Mock()
        self.device.execute.return_value = 'fsck completed with no errors'
        result = execute_fsck(self.device, file_system='harddisk:')
        self.device.execute.assert_called_once_with(
            'fsck harddisk:', timeout=120)
        self.assertEqual(result, 'fsck completed with no errors')

    def test_execute_fsck_custom_timeout(self):
        self.device = Mock()
        self.device.execute.return_value = 'fsck completed with no errors'
        result = execute_fsck(self.device, file_system='bootflash:', timeout=300)
        self.device.execute.assert_called_once_with(
            'fsck bootflash:', timeout=300)
        self.assertEqual(result, 'fsck completed with no errors')

    def test_execute_fsck_subcommandfailure(self):
        self.device = Mock()
        self.device.name = 'DeviceA'
        self.device.execute.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure) as ctx:
            execute_fsck(self.device, file_system='harddisk:')
        self.assertIn(
            'Failed to execute fsck harddisk: on device DeviceA',
            str(ctx.exception)
        )
