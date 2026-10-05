from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1q.configure import unconfigure_interface_switchport_dot1q_tunnel
from unittest.mock import Mock


class TestUnconfigureInterfaceSwitchportDot1qTunnel(TestCase):

    def test_unconfigure_interface_switchport_dot1q_tunnel(self):
        self.device = Mock()
        result = unconfigure_interface_switchport_dot1q_tunnel(self.device, 'Te2/0/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('interface Te2/0/1\n no switchport mode dot1q-tunnel',)
        )
