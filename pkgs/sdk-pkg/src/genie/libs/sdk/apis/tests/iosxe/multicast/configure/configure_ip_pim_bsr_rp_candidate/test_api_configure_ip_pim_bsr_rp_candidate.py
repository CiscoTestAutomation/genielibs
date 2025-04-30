from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_ip_pim_bsr_rp_candidate
from unittest.mock import Mock


class TestConfigureIpPimBsrRpCandidate(TestCase):

    def test_configure_ip_pim_bsr_rp_candidate(self):
        self.device = Mock()
        result = configure_ip_pim_bsr_rp_candidate(self.device, 'Mgmt-vrf', 'GigabitEthernet0/0', 'True', 'True', 'False', 'False')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip pim vrf Mgmt-vrf bsr-candidate GigabitEthernet0/0', 'ip pim vrf Mgmt-vrf rp-candidate GigabitEthernet0/0', 'no ip pim vrf Mgmt-vrf bsr-candidate GigabitEthernet0/0', 'no ip pim vrf Mgmt-vrf rp-candidate GigabitEthernet0/0'],)
        )
