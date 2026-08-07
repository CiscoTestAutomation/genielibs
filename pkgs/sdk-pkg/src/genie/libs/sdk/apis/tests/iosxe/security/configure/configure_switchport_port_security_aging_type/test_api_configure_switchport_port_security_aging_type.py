import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.security.configure import (
    configure_switchport_port_security_aging_type
)


class TestConfigureSwitchportPortSecurityAgingType(unittest.TestCase):

    def test_configure_switchport_port_security_aging_type(self):
        device = Mock()

        result = configure_switchport_port_security_aging_type(
            device,
            'g1/1/1',
            'absolute'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'interface g1/1/1',
                'switchport port-security aging type absolute'
            ],)
        )