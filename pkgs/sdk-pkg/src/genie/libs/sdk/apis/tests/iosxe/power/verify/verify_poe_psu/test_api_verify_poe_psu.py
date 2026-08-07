import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.power.verify import verify_poe_psu


class TestVerifyPoePsu(unittest.TestCase):

    def test_verify_poe_psu(self):
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
        result = verify_poe_psu(device)
        expected_output = True
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
