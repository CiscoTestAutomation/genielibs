from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_pki_vrf_trustpoint
from unittest.mock import Mock


class TestUnconfigurePkiVrfTrustpoint(TestCase):

    def test_unconfigure_pki_vrf_trustpoint(self):
        self.device = Mock()
        result = unconfigure_pki_vrf_trustpoint(self.device, 'client', 'pki')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip vrf pki', 'crypto pki trustpoint client', 'no vrf pki'],)
        )
