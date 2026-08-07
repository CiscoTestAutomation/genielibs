import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.power.verify import verify_total_poe_power


class TestVerifyTotalPoePower(unittest.TestCase):

    def test_verify_total_poe_power(self):
        device = Mock()
        device.api.get_total_poe_power.return_value = 1550.0
        result = verify_total_poe_power(device, 1550.0)
        expected_output = True
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
