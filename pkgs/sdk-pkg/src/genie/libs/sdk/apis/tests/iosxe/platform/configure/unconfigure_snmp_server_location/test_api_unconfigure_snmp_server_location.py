import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_snmp_server_location


class TestUnconfigureSnmpServerLocation(unittest.TestCase):

    def test_unconfigure_snmp_server_location(self):
        device = Mock()

        result = unconfigure_snmp_server_location(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no snmp-server location',)
        )