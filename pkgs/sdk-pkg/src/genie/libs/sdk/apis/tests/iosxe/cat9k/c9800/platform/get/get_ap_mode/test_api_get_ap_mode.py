import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import get_ap_mode


class TestGetApMode(unittest.TestCase):

    def test_get_ap_mode(self):
        device = Mock()
        device.parse.return_value = {
            'ap_name': {
                'AP188B.4500.44C8': {'ap_mode': 'Local'}
            }
        }

        result = get_ap_mode(device, 'AP188B.4500.44C8')

        self.assertEqual(result, 'Local')
        device.parse.assert_called_once_with(
            'show ap name AP188B.4500.44C8 config general'
        )
