from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_role_based_sgt_map_vrf
from unittest.mock import Mock


class TestUnconfigureCtsRoleBasedSgtMapVrf(TestCase):

    def test_unconfigure_cts_role_based_sgt_map_vrf(self):
        self.device = Mock()
        result = unconfigure_cts_role_based_sgt_map_vrf(self.device, 'VRF125', '99.125.1.100', 2211)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts role-based sgt-map vrf VRF125 99.125.1.100 sgt 2211'],)
        )
