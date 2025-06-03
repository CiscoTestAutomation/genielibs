from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_interface_cts_role_based_sgt_map
from unittest.mock import Mock


class TestUnconfigureInterfaceCtsRoleBasedSgtMap(TestCase):

    def test_unconfigure_interface_cts_role_based_sgt_map(self):
        self.device = Mock()
        result = unconfigure_interface_cts_role_based_sgt_map(self.device, 'Gi1/0/4','5', '200')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi1/0/4','no cts role-based sgt-map vlan 5 sgt 200'],)
        )

