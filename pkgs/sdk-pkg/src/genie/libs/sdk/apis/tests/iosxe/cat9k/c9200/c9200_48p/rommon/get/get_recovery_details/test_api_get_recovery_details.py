import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9200.c9200_48p.rommon.get import get_recovery_details


class TestGetRecoveryDetailsBoth(unittest.TestCase):

    def setUp(self):
        
        self.device = Mock()
        self.device.clean = {
            'device_recovery': {
                'tftp_boot': {
                    'image': ['cat9k_iosxe.16.12.1.SPA.bin'],
                    'tftp_server': '15.11.20.02'
                }
            },
            'images': []
        }

        self.device.parse.return_value = {
            'dir': {
                'drec0:': {
                    'files': {
                        'cat9k_iosxe.16.12.1.SPA.bin': {
                            'size': 12345678,
                            'date': 'Jan 01 2020'
                        }
                    }
                }
            }
        }

    def test_get_recovery_details_both(self):
        """Verify both golden image and TFTP boot info are returned."""
        result = get_recovery_details(self.device)

        expected = {
            'golden_image': ['drec0:cat9k_iosxe.16.12.1.SPA.bin'],
            'tftp_boot': {
                'image': ['cat9k_iosxe.16.12.1.SPA.bin'],
                'tftp_server': '15.11.20.02'
            },
            'tftp_image': ['cat9k_iosxe.16.12.1.SPA.bin']
        }
        
        self.assertEqual(result, expected)

