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

    def test_configure_subinterface_dot1q_encapsulation_with_l3_options(self):
        self.device = Mock()
        interface = 'GigabitEthernet1'
        vlan = '100'

        configure_subinterface_dot1q_encapsulation(
            self.device,
            interface=interface,
            vlan=vlan,
            vrf_name='vrf101',
            ip_address='10.1.1.1',
            mask='255.255.255.0',
            no_shutdown=True,
        )

        expected_commands = [
            f"interface {interface}.{vlan}",
            f"encapsulation dot1q {vlan}",
            "ip vrf forwarding vrf101",
            "ip address 10.1.1.1 255.255.255.0",
            "no shutdown",
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

    def test_unconfigure_subinterface_dot1q_encapsulation_remove_subinterface(self):
        self.device = Mock()
        interface = 'GigabitEthernet1'
        vlan = '100'

        unconfigure_subinterface_dot1q_encapsulation(
            self.device,
            interface=interface,
            vlan=vlan,
            remove_subinterface=True,
        )

        expected_commands = [
            f"no interface {interface}.{vlan}",
        ]

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_commands,)
        )
