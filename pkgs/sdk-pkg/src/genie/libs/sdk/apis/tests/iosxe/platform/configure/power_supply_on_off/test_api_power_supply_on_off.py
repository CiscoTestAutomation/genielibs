import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import power_supply_on_off


class TestPowerSupplyOnOff(unittest.TestCase):

    def test_power_supply_on_off(self):
        device = Mock()

        result = power_supply_on_off(device, 1, 'a', 'on')

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('power supply 1 slot a on',)
        )