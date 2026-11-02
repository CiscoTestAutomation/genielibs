import unittest
from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.linux.snmp.configure import configure_snmp_server_view


class TestConfigureSnmpServerViewLinux(TestCase):

    def test_configure_snmp_server_view_default(self):
        """Verify correct CLI with default state (excluded)."""
        device = Mock()
        configure_snmp_server_view(
            device, mib_view='SNMP_RW_VIEW', family_name='iso'
        )
        device.execute.assert_called_once_with(
            'snmp-server view SNMP_RW_VIEW iso excluded'
        )

    def test_configure_snmp_server_view_included(self):
        """Verify correct CLI with state=included."""
        device = Mock()
        configure_snmp_server_view(
            device, mib_view='SNMP_RW_VIEW', family_name='iso',
            state='included'
        )
        device.execute.assert_called_once_with(
            'snmp-server view SNMP_RW_VIEW iso included'
        )

    def test_configure_snmp_server_view_custom_family(self):
        """Verify correct CLI with a specific MIB family OID."""
        device = Mock()
        configure_snmp_server_view(
            device, mib_view='MY_VIEW',
            family_name='1.3.6.1.2.1', state='included'
        )
        device.execute.assert_called_once_with(
            'snmp-server view MY_VIEW 1.3.6.1.2.1 included'
        )

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        device = Mock()
        device.execute.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_snmp_server_view(
                device, mib_view='VIEW1', family_name='iso'
            )


if __name__ == '__main__':
    unittest.main()
