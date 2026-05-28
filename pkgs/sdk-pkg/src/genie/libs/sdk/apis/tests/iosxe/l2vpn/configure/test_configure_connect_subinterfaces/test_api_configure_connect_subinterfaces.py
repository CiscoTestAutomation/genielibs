from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.l2vpn.configure import (
    configure_connect_subinterfaces,
    unconfigure_connect_subinterfaces,
)


class TestConfigureConnectSubinterfaces(TestCase):

    def test_configure_connect_subinterfaces(self):
        self.device = Mock()
        connection_name = 'CONN1'
        interface1 = 'GigabitEthernet1/0/1'
        vlan = 100
        interface2 = 'GigabitEthernet1/0/2'

        configure_connect_subinterfaces(
            self.device,
            connection_name=connection_name,
            interface1=interface1,
            vlan=vlan,
            interface2=interface2
        )

        expected_command = f"connect {connection_name} {interface1}.{vlan} {interface2}.{vlan}"
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_command,)
        )

    def test_unconfigure_connect_subinterfaces(self):
        self.device = Mock()
        connection_name = 'CONN1'
        interface1 = 'GigabitEthernet1/0/1'
        vlan = 100
        interface2 = 'GigabitEthernet1/0/2'

        unconfigure_connect_subinterfaces(
            self.device,
            connection_name=connection_name,
            interface1=interface1,
            vlan=vlan,
            interface2=interface2
        )

        expected_command = f"no connect {connection_name} {interface1}.{vlan} {interface2}.{vlan}"
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_command,)
        )
