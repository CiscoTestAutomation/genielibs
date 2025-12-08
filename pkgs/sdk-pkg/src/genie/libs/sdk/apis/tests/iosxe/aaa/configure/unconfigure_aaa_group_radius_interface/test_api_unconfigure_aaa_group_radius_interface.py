from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_group_radius_interface
from unittest.mock import Mock


class TestUnconfigureAaaGroupRadiusInterface(TestCase):

    def test_unconfigure_aaa_group_radius_interface(self):
        self.device = Mock()
        result = unconfigure_aaa_group_radius_interface(self.device, 'ISE', 'vlan100', 'ip', 'Mgmt-vrf', 'True')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['aaa group server radius ISE', 'no ip vrf forwarding Mgmt-vrf', 'no ip radius source-interface vlan100 vrf Mgmt-vrf'],)
        )
