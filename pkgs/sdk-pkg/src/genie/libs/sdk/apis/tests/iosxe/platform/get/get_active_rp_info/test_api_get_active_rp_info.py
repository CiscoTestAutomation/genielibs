import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.get import get_active_rp_info
from unittest.mock import Mock


class TestGetActiveRpInfo(unittest.TestCase):
    
    def test_get_active_rp_info(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
            'slot': {
                '0': {
                    'rp': {
                        'RP0': {
                            'swstack_role': 'Active',
                            'model': 'CISCO-XYZ',
                            'serial_number': '12345ABC'
                        },
                        'RP1': {
                            'swstack_role': 'Standby',
                            'model': 'CISCO-XYZ',
                            'serial_number': '67890DEF'
                        }
                    }
                }
            }
        })
        expected_output = '0'
        actual_output = get_active_rp_info(self.device)
        self.assertEqual(actual_output, expected_output)