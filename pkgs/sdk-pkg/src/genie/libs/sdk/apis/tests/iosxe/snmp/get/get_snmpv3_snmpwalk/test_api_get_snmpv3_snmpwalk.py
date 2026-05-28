import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.snmp.get import get_snmpv3_snmpwalk


class TestGetSnmpv3SnmpwalkIosxe(TestCase):

    def test_get_snmpv3_snmpwalk_default(self):
        """Verify correct command string with default parameters."""
        device = Mock()
        device.name = 'Router1'
        device.execute.return_value = 'SNMPv2-MIB::sysDescr.0 = STRING: Cisco'
        result = get_snmpv3_snmpwalk(
            device, user_name='SNMPV3_USR', ip_address='10.1.1.1',
            oid='1.3.6.1.2.1.1', auth_password='AuthPass1',
            priv_password='PrivPass1'
        )
        expected_cmd = (
            'snmpwalk -v 3 -l authPriv -u SNMPV3_USR '
            '-a SHA -A AuthPass1 -x AES -X PrivPass1 10.1.1.1 1.3.6.1.2.1.1'
        )
        device.execute.assert_called_once_with(expected_cmd, timeout=60)
        self.assertEqual(result, 'SNMPv2-MIB::sysDescr.0 = STRING: Cisco')

    def test_get_snmpv3_snmpwalk_with_option(self):
        """Verify option is appended to the command."""
        device = Mock()
        device.name = 'Router1'
        device.execute.return_value = 'output'
        result = get_snmpv3_snmpwalk(
            device, user_name='USR1', ip_address='10.2.2.2',
            oid='1.3.6.1', auth_password='Auth1', priv_password='Priv1',
            option='-Oqv'
        )
        expected_cmd = (
            'snmpwalk -v 3 -l authPriv -u USR1 '
            '-a SHA -A Auth1 -x AES -X Priv1 10.2.2.2 1.3.6.1 -Oqv'
        )
        device.execute.assert_called_once_with(expected_cmd, timeout=60)
        self.assertEqual(result, 'output')

    def test_get_snmpv3_snmpwalk_custom_protocols(self):
        """Verify custom auth/priv protocols and security level."""
        device = Mock()
        device.name = 'Router1'
        device.execute.return_value = ''
        get_snmpv3_snmpwalk(
            device, user_name='USR1', ip_address='10.3.3.3',
            oid='1.3.6.1.2.1', auth_password='Auth1', priv_password='Priv1',
            auth_protocol='MD5', priv_protocol='DES',
            security_level='authNoPriv', timeout=120
        )
        expected_cmd = (
            'snmpwalk -v 3 -l authNoPriv -u USR1 '
            '-a MD5 -A Auth1 -x DES -X Priv1 10.3.3.3 1.3.6.1.2.1'
        )
        device.execute.assert_called_once_with(expected_cmd, timeout=120)


if __name__ == '__main__':
    unittest.main()
