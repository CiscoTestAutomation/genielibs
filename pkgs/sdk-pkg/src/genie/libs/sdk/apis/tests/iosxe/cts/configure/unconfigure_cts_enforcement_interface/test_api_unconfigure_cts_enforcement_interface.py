from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_enforcement_interface
from unittest.mock import Mock

class TestUnconfigureCtsEnforcementInterface(TestCase):

    def test_unconfigure_cts_enforcement_interface(self):
        self.device = Mock()
        result = unconfigure_cts_enforcement_interface(self.device, 'TenGigabitEthernet3/0/2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet3/0/2', 'no cts role-based enforcement'],)
        )
