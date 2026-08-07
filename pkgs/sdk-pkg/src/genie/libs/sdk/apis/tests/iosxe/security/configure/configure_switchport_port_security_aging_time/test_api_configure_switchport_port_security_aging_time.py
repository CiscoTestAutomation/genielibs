import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.security.configure import (
    configure_switchport_port_security_aging_time
)


class TestConfigureSwitchportPortSecurityAgingTime(unittest.TestCase):

    def test_configure_switchport_port_security_aging_time(self):
        device = Mock()

        result = configure_switchport_port_security_aging_time(
            device,
            'g1/1/1',
            '40'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'interface g1/1/1',
                'switchport port-security aging time 40'
            ],)
        )