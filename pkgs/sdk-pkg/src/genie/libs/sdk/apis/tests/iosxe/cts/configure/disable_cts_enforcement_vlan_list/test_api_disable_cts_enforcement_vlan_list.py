from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import disable_cts_enforcement_vlan_list
from unittest.mock import Mock

class TestDisableCtsEnforcementVlanList(TestCase):
    
    def test_disable_cts_enforcement_vlan_list(self):
        self.device = Mock()
        result = disable_cts_enforcement_vlan_list(self.device, '1-2047')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts role-based enforcement vlan-list 1-2047'],)
        )