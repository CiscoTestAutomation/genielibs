import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import get_pki_trustpoint_state


class TestGetPkiTrustpointState(unittest.TestCase):

    def test_get_pki_trustpoint_state(self):
        device = Mock()
        expected_output = {
            'certificate_requests': 'yes',
            'issuing_ca_authenticated': 'yes',
            'keys_generated': 'yes'
        }
        device.parse.return_value = {
            'Trustpoints': {
                'vidya-ewlc-5_WLC_TP': {'state': expected_output}
            }
        }

        result = get_pki_trustpoint_state(
            device, 'vidya-ewlc-5_WLC_TP'
        )

        self.assertEqual(result, expected_output)
        device.parse.assert_called_once_with(
            'show crypto pki trustpoint vidya-ewlc-5_WLC_TP status'
        )
