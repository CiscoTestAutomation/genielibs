import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_snmp_server_contact


class TestUnconfigureSnmpServerContact(unittest.TestCase):

    def test_unconfigure_snmp_server_contact(self):
        device = Mock()

        result = unconfigure_snmp_server_contact(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no snmp-server contact',)
        )