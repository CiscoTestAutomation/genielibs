from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_static_nat_source_list_rule

class TestConfigureStaticNatSourceListRule(TestCase):

    def test_configure_static_nat_source_list_rule(self):
        device = Mock()
        result = configure_static_nat_source_list_rule(
            device, 'inside', 'test', 'test1', None, 'vrf_1', 'pap', 'Tw1/0/8', 'oer'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat inside source list test pool test1 vrf vrf_1 oer overload pap',)
        )

    def test_configure_static_nat_source_list_rule_1(self):
        device = Mock()
        result = configure_static_nat_source_list_rule(
            device, 'inside', 'list_in_VRF2', 'pool_in_VRF2', 'Tw1/0/4', 'vrf_1', '', None, None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat inside source list list_in_VRF2 pool pool_in_VRF2 vrf vrf_1 overload',)
        )

    def test_configure_static_nat_source_list_rule_2(self):
        device = Mock()
        result = configure_static_nat_source_list_rule(
            device, 'inside', 'test', None, 'Tw1/0/4', 'vrf_1', '', None, None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat inside source list test interface Tw1/0/4 vrf vrf_1 overload',)
        )

    def test_configure_static_nat_source_list_rule_3(self):
        device = Mock()
        result = configure_static_nat_source_list_rule(
            device, 'inside', 'test', 'test1', None, 'vrf_1', 'egress-interface', 'Tw1/0/8', 'oer'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat inside source list test pool test1 vrf vrf_1 oer overload egress-interface Tw1/0/8',)
        )