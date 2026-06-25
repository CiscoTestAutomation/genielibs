from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.verify import verify_ignore_startup_config


class TestVerifyIgnoreStartupConfig(TestCase):

    def test_verify_ignore_startup_config(self):
        self.device = Mock()
        self.device.is_ha = False
        self.device.subconnections = []
        self.device.parse.return_value = {
            'rommon_variables': {
                'active': {
                    'switch_ignore_startup_config': 1
                }
            }
        }
        self.assertTrue(verify_ignore_startup_config(self.device))
        self.assertEqual(
            self.device.parse.mock_calls[0].args,
            ('show romvar' ,)
        )

    def test_verify_ignore_startup_config_uses_active_connection(self):
        device = Mock()
        device.name = 'mock_device'
        device.is_ha = True
        device.parse.return_value = {
            'rommon_variables': {
                'active': {
                    'switch_ignore_startup_config': 1
                },
                'standby': {
                    'switch_ignore_startup_config': 0
                }
            }
        }

        self.assertTrue(verify_ignore_startup_config(device))
        device.parse.assert_called_once_with('show romvar')

    def test_verify_ignore_startup_config_ignores_empty_standby_value(self):
        device = Mock()
        device.name = 'mock_device'
        device.is_ha = True
        device.parse.return_value = {
            'rommon_variables': {
                'active': {
                    'switch_ignore_startup_config': 0
                },
                'standby': {
                    'mac_addr': '40:CE:24:99:8B:E8'
                }
            }
        }

        self.assertFalse(verify_ignore_startup_config(device))
        device.parse.assert_called_once_with('show romvar')

    def test_verify_ignore_startup_config_parses_active_output_without_standby(self):
        device = Mock()
        device.name = 'mock_device'
        device.is_ha = True
        device.parse.return_value = {
            'rommon_variables': {
                'active': {
                    'switch_ignore_startup_config': 1
                }
            }
        }

        self.assertTrue(verify_ignore_startup_config(device))
        device.parse.assert_called_once_with('show romvar')
