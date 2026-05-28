import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_snmp_server_contact


class TestConfigureSnmpServerContact(unittest.TestCase):

    def test_configure_snmp_server_contact(self):
        device = Mock()

        result = configure_snmp_server_contact(device, 'MAC-ACL')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('snmp-server contact MAC-ACL',)
        )