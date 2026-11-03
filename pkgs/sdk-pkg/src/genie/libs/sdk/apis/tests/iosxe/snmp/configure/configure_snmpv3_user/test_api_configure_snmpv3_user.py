import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.snmp.configure import configure_snmpv3_user


class TestConfigureSnmpv3User(TestCase):

    def test_configure_snmpv3_user_default(self):
        """Verify correct CLI commands for default parameters."""
        device = Mock()
        device.name = 'Router1'
        configure_snmpv3_user(
            device, group_name='SNMPV3_GRP', user_name='SNMPV3_USR',
            auth_password='AuthPass1', priv_password='PrivPass1'
        )
        config_list = device.configure.call_args[0][0]
        self.assertEqual(config_list[0], 'snmp-server group SNMPV3_GRP v3 priv')
        self.assertIn('snmp-server user SNMPV3_USR SNMPV3_GRP v3', config_list[1])
        self.assertIn('auth sha AuthPass1', config_list[1])
        self.assertIn('priv aes 128 PrivPass1', config_list[1])

    def test_configure_snmpv3_user_with_acl(self):
        """Verify ACL is appended to user command."""
        device = Mock()
        device.name = 'Router1'
        configure_snmpv3_user(
            device, group_name='SNMPV3_GRP', user_name='SNMPV3_USR',
            auth_password='AuthPass1', priv_password='PrivPass1',
            acl_name='SNMP_ACL'
        )
        config_list = device.configure.call_args[0][0]
        self.assertIn('access SNMP_ACL', config_list[1])

    def test_configure_snmpv3_user_without_acl(self):
        """Verify no 'access' in command when acl_name is None."""
        device = Mock()
        device.name = 'Router1'
        configure_snmpv3_user(
            device, group_name='SNMPV3_GRP', user_name='SNMPV3_USR',
            auth_password='AuthPass1', priv_password='PrivPass1',
            acl_name=None
        )
        config_list = device.configure.call_args[0][0]
        self.assertNotIn('access', config_list[1])

    def test_configure_snmpv3_user_custom_protocols(self):
        """Verify custom auth/priv protocols."""
        device = Mock()
        device.name = 'Router1'
        configure_snmpv3_user(
            device, group_name='GRP1', user_name='USR1',
            auth_password='Auth1', priv_password='Priv1',
            auth_protocol='md5', priv_protocol='des',
            access_type='auth'
        )
        config_list = device.configure.call_args[0][0]
        self.assertEqual(config_list[0], 'snmp-server group GRP1 v3 auth')
        self.assertIn('auth md5 Auth1', config_list[1])
        self.assertIn('priv des Priv1', config_list[1])

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_snmpv3_user(
                device, group_name='GRP', user_name='USR',
                auth_password='Auth', priv_password='Priv'
            )


    def test_configure_snmpv3_user_with_read_view(self):
        """Verify read view is appended to group command."""
        device = Mock()
        device.name = 'Router1'
        configure_snmpv3_user(
            device, group_name='SNMPV3_GRP', user_name='SNMPV3_USR',
            auth_password='AuthPass1', priv_password='PrivPass1',
            read_view='SNMP_RW_VIEW'
        )
        config_list = device.configure.call_args[0][0]
        self.assertEqual(
            config_list[0],
            'snmp-server group SNMPV3_GRP v3 priv read SNMP_RW_VIEW'
        )

    def test_configure_snmpv3_user_with_write_view(self):
        """Verify write view is appended to group command."""
        device = Mock()
        device.name = 'Router1'
        configure_snmpv3_user(
            device, group_name='SNMPV3_GRP', user_name='SNMPV3_USR',
            auth_password='AuthPass1', priv_password='PrivPass1',
            write_view='SNMP_RW_VIEW'
        )
        config_list = device.configure.call_args[0][0]
        self.assertEqual(
            config_list[0],
            'snmp-server group SNMPV3_GRP v3 priv write SNMP_RW_VIEW'
        )

    def test_configure_snmpv3_user_with_read_and_write_view(self):
        """Verify both read and write views are appended to group command."""
        device = Mock()
        device.name = 'Router1'
        configure_snmpv3_user(
            device, group_name='SNMPV3_GRP', user_name='SNMPV3_USR',
            auth_password='AuthPass1', priv_password='PrivPass1',
            read_view='SNMP_READ_VIEW', write_view='SNMP_WRITE_VIEW'
        )
        config_list = device.configure.call_args[0][0]
        self.assertEqual(
            config_list[0],
            'snmp-server group SNMPV3_GRP v3 priv read SNMP_READ_VIEW write SNMP_WRITE_VIEW'
        )

    def test_configure_snmpv3_user_views_with_acl(self):
        """Verify read/write views and ACL together."""
        device = Mock()
        device.name = 'Router1'
        configure_snmpv3_user(
            device, group_name='SNMPV3_GRP', user_name='SNMPV3_USR',
            auth_password='AuthPass1', priv_password='PrivPass1',
            read_view='SNMP_RW_VIEW', write_view='SNMP_RW_VIEW',
            acl_name='SNMP_ACL'
        )
        config_list = device.configure.call_args[0][0]
        self.assertEqual(
            config_list[0],
            'snmp-server group SNMPV3_GRP v3 priv read SNMP_RW_VIEW write SNMP_RW_VIEW'
        )
        self.assertIn('access SNMP_ACL', config_list[1])


if __name__ == '__main__':
    unittest.main()
