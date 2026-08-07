import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.power.get import get_total_poe_power


class TestGetTotalPoePower(unittest.TestCase):

    def test_get_total_poe_power(self):
        device = Mock()
        device.parse.return_value = {
            'watts': {
                '1': {
                    'module': '1',
                    'available': 1550.0,
                    'used': 147.0,
                    'remaining': 1403.0,
                },
            }
        }
        result = get_total_poe_power(device)
        self.assertEqual(device.parse.call_args.args[0], 'show power inline')
        expected_output = 1550.0
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
