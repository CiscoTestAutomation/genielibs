import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import get_ap_country


class TestGetApCountry(unittest.TestCase):

    def test_get_ap_country(self):
        device = Mock()
        device.parse.return_value = {
            'ap_name': {
                'AP188B.4500.44C8': {'country': 'IN'}
            }
        }

        result = get_ap_country(device, 'AP188B.4500.44C8')

        self.assertEqual(result, 'IN')
        device.parse.assert_called_once_with('show ap summary')
