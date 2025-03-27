from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_ip_pim_bsr_rp_candidate
from unittest.mock import Mock


class TestConfigureIpPimBsrRpCandidate(TestCase):

    def test_configure_ip_pim_bsr_rp_candidate(self):
        self.device = Mock()
        result = configure_ip_pim_bsr_rp_candidate(self.device, 'vrf1', 'Loopback11')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip pim vrf vrf1 bsr-candidate Loopback11', 'ip pim vrf vrf1 rp-candidate Loopback11'],)
        )
