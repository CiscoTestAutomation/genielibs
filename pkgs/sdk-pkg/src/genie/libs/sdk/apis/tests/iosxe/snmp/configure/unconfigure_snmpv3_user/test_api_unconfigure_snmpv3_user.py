import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.snmp.configure import unconfigure_snmpv3_user


class TestUnconfigureSnmpv3User(TestCase):

    def test_unconfigure_snmpv3_user_default(self):
        """Verify correct no-commands with default access_type."""
        device = Mock()
        device.name = 'Router1'
        unconfigure_snmpv3_user(
            device, group_name='SNMPV3_GRP', user_name='SNMPV3_USR'
        )
        config_list = device.configure.call_args[0][0]
        self.assertEqual(config_list[0], 'no snmp-server user SNMPV3_USR SNMPV3_GRP v3')
        self.assertEqual(config_list[1], 'no snmp-server group SNMPV3_GRP v3 priv')

    def test_unconfigure_snmpv3_user_custom_access_type(self):
        """Verify custom access_type in the group removal command."""
        device = Mock()
        device.name = 'Router1'
        unconfigure_snmpv3_user(
            device, group_name='GRP1', user_name='USR1', access_type='auth'
        )
        config_list = device.configure.call_args[0][0]
        self.assertEqual(config_list[0], 'no snmp-server user USR1 GRP1 v3')
        self.assertEqual(config_list[1], 'no snmp-server group GRP1 v3 auth')

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_snmpv3_user(
                device, group_name='GRP', user_name='USR'
            )


if __name__ == '__main__':
    unittest.main()
