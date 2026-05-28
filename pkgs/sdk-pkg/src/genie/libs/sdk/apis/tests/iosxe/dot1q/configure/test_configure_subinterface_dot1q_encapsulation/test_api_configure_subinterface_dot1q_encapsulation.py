from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1q.configure import (
    configure_subinterface_dot1q_encapsulation,
    unconfigure_subinterface_dot1q_encapsulation,
)


class TestConfigureSubinterfaceDot1QEncapsulation(TestCase):

    def test_configure_subinterface_dot1q_encapsulation(self):
        self.device = Mock()
        interface = 'GigabitEthernet1'
        vlan = '100'

        configure_subinterface_dot1q_encapsulation(self.device, interface=interface, vlan=vlan)

        expected_commands = [
            f"interface {interface}.{vlan}",
            f"encapsulation dot1q {vlan}"
        ]

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_commands,)
        )

    def test_unconfigure_subinterface_dot1q_encapsulation(self):
        self.device = Mock()
        interface = 'GigabitEthernet1'
        vlan = '100'

        unconfigure_subinterface_dot1q_encapsulation(self.device, interface=interface, vlan=vlan)

        expected_commands = [
            f"interface {interface}.{vlan}",
            f"no encapsulation dot1q {vlan}"
        ]

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_commands,)
        )
