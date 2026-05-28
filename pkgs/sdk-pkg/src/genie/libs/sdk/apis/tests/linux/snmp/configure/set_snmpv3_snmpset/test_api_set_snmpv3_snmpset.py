import unittest
from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.linux.snmp.configure import set_snmpv3_snmpset


class TestSetSnmpv3SnmpsetLinux(TestCase):

    def test_set_snmpv3_snmpset_default(self):
        """Verify correct command string with default parameters."""
        device = Mock()
        device.name = 'linux1'
        device.execute.return_value = 'SNMPv2-MIB::sysContact.0 = STRING: admin'
        result = set_snmpv3_snmpset(
            device, user_name='SNMPV3_USR', ip_address='10.1.1.1',
            oid='1.3.6.1.2.1.1.4.0', auth_password='AuthPass1',
            priv_password='PrivPass1'
        )
        expected_cmd = (
            'snmpset -v 3 -l authPriv -u SNMPV3_USR '
            '-a SHA -A AuthPass1 -x AES -X PrivPass1 10.1.1.1 1.3.6.1.2.1.1.4.0'
        )
        device.execute.assert_called_once_with(expected_cmd)
        self.assertEqual(result, 'SNMPv2-MIB::sysContact.0 = STRING: admin')

    def test_set_snmpv3_snmpset_with_string(self):
        """Verify string value is appended with 's' type."""
        device = Mock()
        device.name = 'linux1'
        device.execute.return_value = 'ok'
        set_snmpv3_snmpset(
            device, user_name='USR1', ip_address='10.2.2.2',
            oid='1.3.6.1.2.1.1.4.0', auth_password='Auth1',
            priv_password='Priv1', string='admin@cisco.com'
        )
        expected_cmd = (
            'snmpset -v 3 -l authPriv -u USR1 '
            '-a SHA -A Auth1 -x AES -X Priv1 10.2.2.2 '
            '1.3.6.1.2.1.1.4.0 s admin@cisco.com'
        )
        device.execute.assert_called_once_with(expected_cmd)

    def test_set_snmpv3_snmpset_with_option(self):
        """Verify option is appended to the command."""
        device = Mock()
        device.name = 'linux1'
        device.execute.return_value = 'ok'
        set_snmpv3_snmpset(
            device, user_name='USR1', ip_address='10.2.2.2',
            oid='1.3.6.1.2.1.1.4.0', auth_password='Auth1',
            priv_password='Priv1', option='i 2'
        )
        expected_cmd = (
            'snmpset -v 3 -l authPriv -u USR1 '
            '-a SHA -A Auth1 -x AES -X Priv1 10.2.2.2 '
            '1.3.6.1.2.1.1.4.0 i 2'
        )
        device.execute.assert_called_once_with(expected_cmd)

    def test_set_snmpv3_snmpset_string_and_option(self):
        """Verify both string and option are appended."""
        device = Mock()
        device.name = 'linux1'
        device.execute.return_value = 'ok'
        set_snmpv3_snmpset(
            device, user_name='USR1', ip_address='10.2.2.2',
            oid='1.3.6.1.2.1.1.4.0', auth_password='Auth1',
            priv_password='Priv1', string='test', option='-r 3'
        )
        expected_cmd = (
            'snmpset -v 3 -l authPriv -u USR1 '
            '-a SHA -A Auth1 -x AES -X Priv1 10.2.2.2 '
            '1.3.6.1.2.1.1.4.0 s test -r 3'
        )
        device.execute.assert_called_once_with(expected_cmd)

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        device = Mock()
        device.name = 'linux1'
        device.execute.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            set_snmpv3_snmpset(
                device, user_name='USR1', ip_address='10.1.1.1',
                oid='1.3.6.1.2.1.1.4.0', auth_password='Auth1',
                priv_password='Priv1'
            )


if __name__ == '__main__':
    unittest.main()
