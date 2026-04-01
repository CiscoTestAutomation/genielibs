from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nve.configure import unconfig_nve_vni_members

class TestUnconfigNveVniMembers(TestCase):

    def test_unconfig_nve_vni_members_l3vni(self):
        device = Mock()
        vni_cfg = {50000: {'vrf_name': 'red'}}
        result = unconfig_nve_vni_members(device, "nve 1", vni_cfg)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface nve 1', 'no member vni 50000 vrf red'],)
        )

    def test_unconfig_nve_vni_members_l2vni_static(self):
        device = Mock()
        vni_cfg = {20000: {'mcast_group': '225.1.1.1'}}
        result = unconfig_nve_vni_members(device, "nve 1", vni_cfg)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface nve 1', 'no member vni 20000 mcast-group 225.1.1.1'],)
        )

    def test_unconfig_nve_vni_members_l2vni_ir(self):
        device = Mock()
        vni_cfg = {30000: {'is_ingress_rep': True}}
        result = unconfig_nve_vni_members(device, "nve 1", vni_cfg)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface nve 1', 'no member vni 30000 ingress-replication'],)
        )