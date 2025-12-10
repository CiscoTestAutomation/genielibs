import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.get import get_power_supply_status
from unittest.mock import Mock


class TestGetPowerSupplyStatus(unittest.TestCase):

   
    def test_get_power_supply_status(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
            'power_supplies': {
                'PS1': {
                    'status': 'ok',
                    'type': 'AC',
                    'voltage': '120V'
                },
                'PS2': {
                    'status': 'failed',
                    'type': 'DC',
                    'voltage': '0V'
                }
            }
        })
        expected_output = {
            'PS1': {
                'status': 'ok',
                'type': 'AC',
                'voltage': '120V'
            },
            'PS2': {
                'status': 'failed',
                'type': 'DC',
                'voltage': '0V'
            }
        }
        actual_output = get_power_supply_status(self.device)
        self.assertEqual(actual_output, expected_output)