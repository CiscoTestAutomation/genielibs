from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_interface_vrf
from unittest.mock import Mock


class TestConfigureRadiusInterfaceVrf(TestCase):

    def test_configure_radius_interface_vrf(self):
        self.device = Mock()
        result = configure_radius_interface_vrf(self.device, 'gig0/0', 'Mgmt-vrf', 'ipv6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 radius source-interface gig0/0 vrf Mgmt-vrf'],)
        )
