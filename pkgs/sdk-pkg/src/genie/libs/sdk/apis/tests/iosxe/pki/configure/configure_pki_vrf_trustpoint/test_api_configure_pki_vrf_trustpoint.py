from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_vrf_trustpoint
from unittest.mock import Mock


class TestConfigurePkiVrfTrustpoint(TestCase):

    def test_configure_pki_vrf_trustpoint(self):
        self.device = Mock()
        result = configure_pki_vrf_trustpoint(self.device, 'client', 'pki')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip vrf pki', 'crypto pki trustpoint client', 'vrf pki'],)
        )
