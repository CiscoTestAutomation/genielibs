from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_group
from unittest.mock import Mock


class TestConfigureRadiusGroup(TestCase):

    def test_configure_radius_group(self):
        self.device = Mock()
        result = configure_radius_group(self.device, {'ipv6_intf': 'Vlan999', 'server_group': 'ISEGRP', 'server_name': 'ipv6_server'})
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['aaa group server radius ISEGRP', 'server name ipv6_server', 'ipv6 radius source-interface Vlan999', 'radius server ipv6_server'],)
        )
