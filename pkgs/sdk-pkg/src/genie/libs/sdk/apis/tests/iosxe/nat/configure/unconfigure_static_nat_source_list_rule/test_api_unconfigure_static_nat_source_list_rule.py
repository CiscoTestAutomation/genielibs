from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_static_nat_source_list_rule

class TestUnconfigureStaticNatSourceListRule(TestCase):

    def test_unconfigure_static_nat_source_list_rule(self):
        device = Mock()
        result = unconfigure_static_nat_source_list_rule(
            device, 'inside', 'test', 'test1', None, 'vrf_1', 'pap', 'Gi1/0/16', 'oer'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat inside source list test pool test1 vrf vrf_1 oer overload pap',)
        )

    def test_unconfigure_static_nat_source_list_rule_1(self):
        device = Mock()
        result = unconfigure_static_nat_source_list_rule(
            device, 'inside', 'list_in_VRF2', 'pool_in_VRF2', 'Gi1/0/16', 'vrf_1', '', None, None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat inside source list list_in_VRF2 pool pool_in_VRF2 vrf vrf_1 overload',)
        )

    def test_unconfigure_static_nat_source_list_rule_2(self):
        device = Mock()
        result = unconfigure_static_nat_source_list_rule(
            device, 'inside', 'test', None, 'Gi1/0/16', 'vrf_1', '', None, None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat inside source list test interface Gi1/0/16 vrf vrf_1 overload',)
        )