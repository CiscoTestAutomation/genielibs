from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_pnp_startup_vlan
from unittest.mock import Mock


class TestUnconfigurePnpStartupVlan(TestCase):

    def test_unconfigure_pnp_startup_vlan(self):
        self.device = Mock()
        result = unconfigure_pnp_startup_vlan(self.device, '1200', 'GigabitEthernet1/0/10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/10', 'no pnp startup-vlan 1200'],)
        )
