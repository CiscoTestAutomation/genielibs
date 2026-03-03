from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_role_based_sgt_map_vrf
from unittest.mock import Mock


class TestConfigureCtsRoleBasedSgtMapVrf(TestCase):

    def test_configure_cts_role_based_sgt_map_vrf(self):
        self.device = Mock()
        result = configure_cts_role_based_sgt_map_vrf(self.device, 'VRF125', '99.125.1.100', 2211)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts role-based sgt-map vrf VRF125 99.125.1.100 sgt 2211'],)
        )
