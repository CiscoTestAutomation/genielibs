import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.snmp.configure import unconfigure_snmp_server_host


class TestUnconfigureSnmpServerHost(unittest.TestCase):

    def test_unconfigure_snmp_server_host(self):
        device = Mock()

        result = unconfigure_snmp_server_host(
            device,
            '5.5.5.5',
            6,
            '[QggBEaZ^MSMV`ATHVFB]Pcd^Z`O`\\',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server host 5.5.5.5 6 [QggBEaZ^MSMV`ATHVFB]Pcd^Z`O`\\'
        )

    def test_unconfigure_snmp_server_host_without_version(self):
        device = Mock()

        result = unconfigure_snmp_server_host(device, '10.1.1.1', 'public')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no snmp-server host 10.1.1.1 public')
