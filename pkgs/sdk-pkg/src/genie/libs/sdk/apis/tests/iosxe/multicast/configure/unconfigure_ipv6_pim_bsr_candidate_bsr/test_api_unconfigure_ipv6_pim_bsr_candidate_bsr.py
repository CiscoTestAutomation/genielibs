from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_pim_bsr_candidate_bsr
from unittest.mock import Mock


class TestUnconfigureIpv6PimBsrCandidateBsr(TestCase):

    def test_unconfigure_ipv6_pim_bsr_candidate_bsr(self):
        self.device = Mock()
        result = unconfigure_ipv6_pim_bsr_candidate_bsr(self.device, '2001::1', 'Mgmt-vrf', '254')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ipv6 pim vrf Mgmt-vrf bsr candidate bsr 2001::1 priority 254',)
        )
