from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.snmp.configure import (
    configure_debug_snmp_packets,
)


class TestConfigureDebugSnmpPackets(TestCase):

    def test_configure_debug_snmp_packets(self):
        device = Mock()
        result = configure_debug_snmp_packets(device)
        self.assertIsNone(result)
        device.execute.assert_called_once_with('debug snmp packets')
