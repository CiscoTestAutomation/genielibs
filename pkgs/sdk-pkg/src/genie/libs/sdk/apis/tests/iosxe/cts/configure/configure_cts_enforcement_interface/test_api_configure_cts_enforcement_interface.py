from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_enforcement_interface
from unittest.mock import Mock

class TestConfigureCtsEnforcementInterface(TestCase):

    def test_configure_cts_enforcement_interface(self):
        self.device = Mock()
        configure_cts_enforcement_interface(self.device, 'TenGigabitEthernet3/0/2')
        self.assertEqual(self.device.configure.mock_calls[0].args,(["interface TenGigabitEthernet3/0/2","cts role-based enforcement"],))