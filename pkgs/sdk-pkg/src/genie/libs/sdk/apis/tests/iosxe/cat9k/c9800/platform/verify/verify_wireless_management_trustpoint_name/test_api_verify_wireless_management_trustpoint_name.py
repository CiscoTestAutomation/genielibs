import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import verify_wireless_management_trustpoint_name


class TestVerifyWirelessManagementTrustpointName(unittest.TestCase):

    def test_verify_wireless_management_trustpoint_name(self):
        device = Mock()
        device.api.get_wireless_management_trustpoint_name.return_value = (
            'vidya-ewlc-5_WLC_TP'
        )

        result = verify_wireless_management_trustpoint_name(
            device, 'vidya-ewlc-5_WLC_TP', 60, 10
        )

        self.assertTrue(result)
        device.api.get_wireless_management_trustpoint_name.assert_called_once_with()
