import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import get_ap_model


class TestGetApModel(unittest.TestCase):

    def test_get_ap_model(self):
        device = Mock()
        device.parse.return_value = {
            'ap_name': {
                'AP188B.4500.44C8': {'ap_model': 'AIR-AP1832I-D-K9'}
            }
        }

        result = get_ap_model(device, 'AP188B.4500.44C8')

        self.assertEqual(result, 'AIR-AP1832I-D-K9')
        device.parse.assert_called_once_with('show ap summary')
