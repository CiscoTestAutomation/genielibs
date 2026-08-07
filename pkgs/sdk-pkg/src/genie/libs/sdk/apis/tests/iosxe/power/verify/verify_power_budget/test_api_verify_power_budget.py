import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.power.verify import verify_power_budget


class TestVerifyPowerBudget(unittest.TestCase):

    def test_verify_power_budget(self):
        device = Mock()
        device.api.get_power_budget.return_value = (147.0, 1403.0)
        result = verify_power_budget(
            device, max_used_watts=200.0, min_remain_watts=1000.0
        )
        expected_output = True
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
