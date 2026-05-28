import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.snmp.configure import configure_snmp_server_host


class TestConfigureSnmpServerHost(unittest.TestCase):

    def test_configure_snmp_server_host(self):
        device = Mock()

        result = configure_snmp_server_host(
            device,
            '5.5.5.5',
            6,
            '[QggBEaZ^MSMV`ATHVFB]Pcd^Z`O`\\',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'snmp-server host 5.5.5.5 6 [QggBEaZ^MSMV`ATHVFB]Pcd^Z`O`\\'
        )

    def test_configure_snmp_server_host_without_version(self):
        device = Mock()

        result = configure_snmp_server_host(device, '10.1.1.2', 'public')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('snmp-server host 10.1.1.2 public')
