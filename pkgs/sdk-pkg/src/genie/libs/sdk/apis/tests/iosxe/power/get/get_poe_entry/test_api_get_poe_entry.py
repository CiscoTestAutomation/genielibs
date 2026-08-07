import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.power.get import get_poe_entry


class TestGetPoeEntry(unittest.TestCase):

    def test_get_poe_entry(self):
        device = Mock()
        device.parse.return_value = {
            'interface': {
                'GigabitEthernet1/0/1': {
                    'admin_state': 'auto',
                    'oper_state': 'on',
                    'power': 15.4,
                    'max': 30.0,
                    'class': '3',
                    'device': 'IP Phone 8845',
                },
                'GigabitEthernet1/0/2': {
                    'admin_state': 'auto',
                    'oper_state': 'off',
                    'power': 0.0,
                    'max': 30.0,
                    'class': 'n/a',
                    'device': 'n/a',
                },
            }
        }
        result = get_poe_entry(device, 'GigabitEthernet1/0/1')
        self.assertEqual(device.parse.call_args.args[0], 'show power inline')
        expected_output = {
            'mode': 'auto',
            'op_state': 'on',
            'power': 15.4,
            'max': 30.0,
            'class': '3',
            'desc': 'IP Phone 8845',
        }
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
