from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.security.configure import (
    configure_switchport_port_security_maximum,
)


class TestConfigureSwitchportPortSecurityMaximum(TestCase):

    def test_configure_switchport_port_security_maximum(self):
        device = Mock()

        result = configure_switchport_port_security_maximum(
            device=device,
            interface='g1/1/1',
            address='1000',
            vlan_type=None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'interface g1/1/1',
            'switchport port-security maximum 1000',
        ])

    def test_configure_switchport_port_security_maximum_1(self):
        device = Mock()

        result = configure_switchport_port_security_maximum(
            device=device,
            interface='g1/1/1',
            address='1000',
            vlan_type='access',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'interface g1/1/1',
            'switchport port-security maximum 1000 vlan access',
        ])
