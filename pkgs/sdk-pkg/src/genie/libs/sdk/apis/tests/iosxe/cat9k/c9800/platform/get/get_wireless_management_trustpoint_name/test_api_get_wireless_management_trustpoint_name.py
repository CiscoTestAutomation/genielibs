import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import get_wireless_management_trustpoint_name


class TestGetWirelessManagementTrustpointName(unittest.TestCase):

    def test_get_wireless_management_trustpoint_name(self):
        device = Mock()
        parsed_output = Mock()
        parsed_output.q.get_values.return_value = 'vidya-ewlc-5_WLC_TP'
        device.parse.return_value = parsed_output

        result = get_wireless_management_trustpoint_name(device)

        self.assertEqual(result, 'vidya-ewlc-5_WLC_TP')
        device.parse.assert_called_once_with(
            'show wireless management trustpoint'
        )
        parsed_output.q.get_values.assert_called_once_with(
            'trustpoint_name', 0
        )
