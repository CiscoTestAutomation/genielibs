from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cts.configure import configure_interface_cts_role_based_sgt_map


class TestConfigureInterfaceCtsRoleBasedSgtMap(TestCase):
    def test_configure_interface_cts_role_based_sgt_map(self):
        device = Mock()
        result = configure_interface_cts_role_based_sgt_map(device, 'Gi1/0/4', 5, 200)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Gi1/0/4', 
              'cts role-based sgt-map vlan 5 sgt 200'],)
        )