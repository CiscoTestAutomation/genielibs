from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_v4_list_pool_overload

class TestConfigureNat64V4ListPoolOverload(TestCase):

    def test_configure_nat64_v4_list_pool_overload(self):
        device = Mock()
        result = configure_nat64_v4_list_pool_overload(device, 'acl_1', 'pool_1', 'vrf1', 'match-in-vrf')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('nat64 v6v4 list acl_1 pool pool_1 vrf vrf1 overload match-in-vrf',)
        )