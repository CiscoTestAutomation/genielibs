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

    def test_get_power_supply_status_all_switches(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
            'switch': {
                '1': {
                    'power_supplies': {
                        'PS1': {
                            'status': 'ok',
                            'pid': 'PID123',
                            'serial': 'SN123',
                            'sys_pwr': 'yes',
                            'watts': 500
                        }
                    }
                },
                '2': {
                    'power_supplies': {
                        'PS2': {
                            'status': 'failed',
                            'pid': 'PID456',
                            'serial': 'SN456',
                            'sys_pwr': 'no',
                            'watts': 0
                        }
                    }
                }
            }
        })
        expected_output = {
            'Switch 1 - PS1': {
                'status': 'ok',
                'pid': 'PID123',
                'serial': 'SN123',
                'sys_pwr': 'yes',
                'watts': 500
            },
            'Switch 2 - PS2': {
                'status': 'failed',
                'pid': 'PID456',
                'serial': 'SN456',
                'sys_pwr': 'no',
                'watts': 0
            }
        }
        actual_output = get_power_supply_status(self.device, all_switches=True)
        self.assertEqual(actual_output, expected_output)
