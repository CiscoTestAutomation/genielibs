import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_snmp_server_location


class TestConfigureSnmpServerLocation(unittest.TestCase):

    def test_configure_snmp_server_location(self):
        device = Mock()

        result = configure_snmp_server_location(device, 'Test lab')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('snmp-server location Test lab',)
        )