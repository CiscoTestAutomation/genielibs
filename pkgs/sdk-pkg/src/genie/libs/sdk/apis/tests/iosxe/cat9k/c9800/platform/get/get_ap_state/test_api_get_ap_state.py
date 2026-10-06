import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import get_ap_state


class TestGetApState(unittest.TestCase):

    def test_get_ap_state(self):
        device = Mock()
        device.parse.return_value = {
            'ap_name': {
                'AP188B.4500.44C8': {'state': 'Registered'}
            }
        }

        result = get_ap_state(device, 'AP188B.4500.44C8')

        self.assertEqual(result, 'Registered')
        device.parse.assert_called_once_with('show ap summary')
