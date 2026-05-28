import unittest
from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.linux.snmp.get import get_snmpv3_snmpget


class TestGetSnmpv3SnmpgetLinux(TestCase):

    def test_get_snmpv3_snmpget_default(self):
        """Verify correct command string with default parameters."""
        device = Mock()
        device.name = 'linux1'
        device.execute.return_value = 'SNMPv2-MIB::sysDescr.0 = STRING: Linux'
        result = get_snmpv3_snmpget(
            device, user_name='SNMPV3_USR', ip_address='10.1.1.1',
            oid='1.3.6.1.2.1.1.1.0', auth_password='AuthPass1',
            priv_password='PrivPass1'
        )
        expected_cmd = (
            'snmpget -v 3 -l authPriv -u SNMPV3_USR '
            '-a SHA -A AuthPass1 -x AES -X PrivPass1 10.1.1.1 1.3.6.1.2.1.1.1.0'
        )
        device.execute.assert_called_once_with(expected_cmd)
        self.assertEqual(result, 'SNMPv2-MIB::sysDescr.0 = STRING: Linux')

    def test_get_snmpv3_snmpget_with_option(self):
        """Verify option is appended to the command."""
        device = Mock()
        device.name = 'linux1'
        device.execute.return_value = 'output'
        result = get_snmpv3_snmpget(
            device, user_name='USR1', ip_address='10.2.2.2',
            oid='1.3.6.1.2.1.1.1.0', auth_password='Auth1',
            priv_password='Priv1', option='-Oqv'
        )
        expected_cmd = (
            'snmpget -v 3 -l authPriv -u USR1 '
            '-a SHA -A Auth1 -x AES -X Priv1 10.2.2.2 1.3.6.1.2.1.1.1.0 -Oqv'
        )
        device.execute.assert_called_once_with(expected_cmd)
        self.assertEqual(result, 'output')

    def test_get_snmpv3_snmpget_custom_protocols(self):
        """Verify custom auth/priv protocols and security level."""
        device = Mock()
        device.name = 'linux1'
        device.execute.return_value = ''
        get_snmpv3_snmpget(
            device, user_name='USR1', ip_address='10.3.3.3',
            oid='1.3.6.1.2.1.1.3.0', auth_password='Auth1',
            priv_password='Priv1', auth_protocol='MD5',
            priv_protocol='DES', security_level='authNoPriv'
        )
        expected_cmd = (
            'snmpget -v 3 -l authNoPriv -u USR1 '
            '-a MD5 -A Auth1 -x DES -X Priv1 10.3.3.3 1.3.6.1.2.1.1.3.0'
        )
        device.execute.assert_called_once_with(expected_cmd)

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        device = Mock()
        device.name = 'linux1'
        device.execute.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            get_snmpv3_snmpget(
                device, user_name='USR1', ip_address='10.1.1.1',
                oid='1.3.6.1.2.1.1.1.0', auth_password='Auth1',
                priv_password='Priv1'
            )


if __name__ == '__main__':
    unittest.main()
