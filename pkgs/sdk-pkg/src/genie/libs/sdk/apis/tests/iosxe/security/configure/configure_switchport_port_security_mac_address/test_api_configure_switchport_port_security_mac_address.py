import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.security.configure import (
    configure_switchport_port_security_mac_address
)


class TestConfigureSwitchportPortSecurityMacAddress(unittest.TestCase):

    def test_configure_switchport_port_security_mac_address(self):
        device = Mock()

        result = configure_switchport_port_security_mac_address(
            device,
            'g1/1/1',
            'sticky',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'interface g1/1/1',
                'switchport port-security mac-address sticky'
            ],)
        )

    def test_configure_switchport_port_security_mac_address_1(self):
        device = Mock()

        result = configure_switchport_port_security_mac_address(
            device,
            'g1/1/1',
            '0001.0001.000c',
            'voice'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'interface g1/1/1',
                'switchport port-security mac-address 0001.0001.000c vlan voice'
            ],)
        )