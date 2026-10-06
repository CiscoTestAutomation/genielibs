import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import verify_pki_trustpoint_state


class TestVerifyPkiTrustpointState(unittest.TestCase):

    def test_verify_pki_trustpoint_state(self):
        device = Mock()
        device.api.get_pki_trustpoint_state.return_value = {
            'certificate_requests': 'yes',
            'issuing_ca_authenticated': 'yes',
            'keys_generated': 'yes'
        }

        result = verify_pki_trustpoint_state(
            device, 'vidya-ewlc-5_WLC_TP', 60, 10
        )

        self.assertTrue(result)
        device.api.get_pki_trustpoint_state.assert_called_once_with(
            trustpoint_name='vidya-ewlc-5_WLC_TP'
        )
