import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.power.verify import verify_poe_entry_op_state


class TestVerifyPoeEntryOpState(unittest.TestCase):

    def test_verify_poe_entry_op_state(self):
        device = Mock()
        device.api.get_poe_entry.return_value = {
            'mode': 'auto',
            'op_state': 'on',
            'power': 15.4,
            'max': 30.0,
            'class': '3',
            'desc': 'IP Phone 8845',
        }
        result = verify_poe_entry_op_state(
            device, 'GigabitEthernet1/0/1', 'on'
        )
        expected_output = True
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
