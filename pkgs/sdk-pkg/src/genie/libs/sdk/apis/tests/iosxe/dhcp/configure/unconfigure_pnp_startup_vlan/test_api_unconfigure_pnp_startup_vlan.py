from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_pnp_startup_vlan
from unittest.mock import Mock

class TestUnconfigurePnpStartupVlan(TestCase):

    def test_unconfigure_pnp_startup_vlan(self):
        self.device = Mock()
        unconfigure_pnp_startup_vlan(self.device, 501)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no pnp startup-vlan 501',)
        )
