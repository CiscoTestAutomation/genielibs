import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_snmp_server_manager


class TestConfigureSnmpServerManager(unittest.TestCase):

    def test_configure_snmp_server_manager(self):
        device = Mock()

        result = configure_snmp_server_manager(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('snmp-server manager',)
        )