from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_pim_bsr_candidate_rp
from unittest.mock import Mock


class TestUnconfigureIpv6PimBsrCandidateRp(TestCase):

    def test_unconfigure_ipv6_pim_bsr_candidate_rp(self):
        self.device = Mock()
        result = unconfigure_ipv6_pim_bsr_candidate_rp(self.device, '2001::1', 'Mgmt-vrf', '190')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ipv6 pim vrf Mgmt-vrf bsr candidate rp 2001::1 priority 190',)
        )
