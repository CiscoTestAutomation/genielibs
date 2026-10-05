from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.snmp.configure import configure_logging_snmp_trap


class TestConfigureLoggingSnmpTrap(TestCase):

    def test_configure_logging_snmp_trap(self):
        device = Mock()
        result = configure_logging_snmp_trap(device, 'warnings')
        self.assertIsNone(result)
        device.configure.assert_called_once_with('logging snmp-trap warnings')
