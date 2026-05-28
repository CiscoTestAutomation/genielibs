import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.utils import get_show_output_include
from unicon.core.errors import SubCommandFailure


class TestGetShowOutputInclude(unittest.TestCase):

    def test_get_show_output_include(self):
        device = Mock()
        device.execute.return_value = 'ip ospf 100 area 0'
        result = get_show_output_include(device, 'show running-config', 'ospf')
        device.execute.assert_called_once_with(
            'show running-config | include ospf'
        )
        self.assertEqual(result, [True, 'ip ospf 100 area 0'])

    def test_get_show_output_include_no_match(self):
        device = Mock()
        device.execute.return_value = ''
        result = get_show_output_include(device, 'show running-config', 'ospf')
        self.assertEqual(result, [False, ''])

    def test_get_show_output_include_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure('Test error')
        result = get_show_output_include(device, 'show running-config', 'ospf')
        self.assertEqual(result[0], False)


if __name__ == '__main__':
    unittest.main()
