import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.power.get import get_power_budget


class TestGetPowerBudget(unittest.TestCase):

    def test_get_power_budget(self):
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
        result = get_power_budget(device)
        self.assertEqual(device.parse.call_args.args[0], 'show power inline')
        expected_output = (147.0, 1403.0)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
