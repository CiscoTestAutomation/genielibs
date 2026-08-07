import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.utils import get_show_output
from unicon.core.errors import SubCommandFailure


class TestGetShowOutput(unittest.TestCase):

    def test_get_show_output_without_target(self):
        device = Mock()
        device.execute.return_value = 'some output'
        result = get_show_output(device, 'show version')
        device.execute.assert_called_once_with('show version')
        self.assertEqual(result, (True, 'some output'))

    def test_get_show_output_with_target(self):
        device = Mock()
        device.execute.return_value = 'some output'
        result = get_show_output(device, 'show version', target='standby')
        device.execute.assert_called_once_with('show version', target='standby')
        self.assertEqual(result, (True, 'some output'))

    def test_get_show_output_empty_output_returns_false(self):
        device = Mock()
        device.execute.return_value = ''
        result = get_show_output(device, 'show version')
        self.assertEqual(result, (False, ''))

    def test_get_show_output_failure(self):
        device = Mock()
        device.name = 'uut'
        device.execute.side_effect = SubCommandFailure('Test error')
        with self.assertRaises(SubCommandFailure):
            get_show_output(device, 'show version')


if __name__ == '__main__':
    unittest.main()
