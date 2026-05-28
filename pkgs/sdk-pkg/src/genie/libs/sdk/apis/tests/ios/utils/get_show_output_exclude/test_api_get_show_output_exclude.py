import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.utils import get_show_output_exclude
from unicon.core.errors import SubCommandFailure


class TestGetShowOutputExclude(unittest.TestCase):

    def test_get_show_output_exclude(self):
        device = Mock()
        device.execute.return_value = 'ip address 10.0.0.1 255.255.255.0'
        result = get_show_output_exclude(device, 'show running-config', 'ospf')
        device.execute.assert_called_once_with(
            'show running-config | exclude ospf'
        )
        self.assertEqual(result, [True, 'ip address 10.0.0.1 255.255.255.0'])

    def test_get_show_output_exclude_no_match(self):
        device = Mock()
        device.execute.return_value = ''
        result = get_show_output_exclude(device, 'show running-config', 'ospf')
        self.assertEqual(result, [False, ''])

    def test_get_show_output_exclude_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure('Test error')
        result = get_show_output_exclude(device, 'show running-config', 'ospf')
        self.assertEqual(result[0], False)


if __name__ == '__main__':
    unittest.main()
