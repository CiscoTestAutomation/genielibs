from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1q.configure import configure_interface_switchport_dot1q_tunnel
from unittest.mock import Mock


class TestConfigureInterfaceSwitchportDot1qTunnel(TestCase):

    def test_configure_interface_switchport_dot1q_tunnel(self):
        self.device = Mock()
        result = configure_interface_switchport_dot1q_tunnel(self.device, 'Te2/0/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('interface Te2/0/1\n switchport mode dot1q-tunnel',)
        )
