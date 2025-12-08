from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_radius_interface_vrf
from unittest.mock import Mock


class TestUnconfigureRadiusInterfaceVrf(TestCase):

    def test_unconfigure_radius_interface_vrf(self):
        self.device = Mock()
        result = unconfigure_radius_interface_vrf(self.device, 'gig0/0', 'Mgmt-vrf', 'ipv6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 radius source-interface gig0/0 vrf Mgmt-vrf'],)
        )
