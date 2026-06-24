import unittest
from unittest.mock import MagicMock

from genie.libs.sdk.apis.iosxe.snmp.configure import (
    configure_snmp_server_trap,
    unconfigure_snmp_server_trap,
    unconfigure_snmp_server_group,
    unconfigure_snmp_server_user,
)
from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_ip_ssh_version,
)


class TestConfigureSnmpServerTrapCategoryWithSpace(unittest.TestCase):

    def test_snmp_linkdown_accepted(self):
        device = MagicMock()
        configure_snmp_server_trap(device, trap_type='snmp linkdown')
        device.configure.assert_called_once_with(
            ['snmp-server enable traps snmp linkdown'])

    def test_unsafe_trap_type_rejected(self):
        device = MagicMock()
        with self.assertRaises(ValueError):
            configure_snmp_server_trap(
                device, trap_type='snmp\nno snmp-server')
        device.configure.assert_not_called()


class TestUnconfigureSnmpServerTrapCategoryWithSpace(unittest.TestCase):

    def test_snmp_linkdown_accepted(self):
        device = MagicMock()
        unconfigure_snmp_server_trap(device, trap_type='snmp linkdown')
        device.configure.assert_called_once_with(
            ['no snmp-server enable traps snmp linkdown'])

    def test_unsafe_trap_type_rejected(self):
        device = MagicMock()
        with self.assertRaises(ValueError):
            unconfigure_snmp_server_trap(
                device, trap_type='snmp\nno snmp-server')
        device.configure.assert_not_called()


class TestUnconfigureSnmpServerGroupEmptyAuthType(unittest.TestCase):

    def test_empty_auth_type_accepted(self):
        device = MagicMock()
        unconfigure_snmp_server_group(
            device, group_name='g1', version='v3', auth_type='')
        device.configure.assert_called_once()


class TestUnconfigureSnmpServerUserNonV3(unittest.TestCase):

    def test_v2c_user_with_auth_type_does_not_raise(self):
        device = MagicMock()
        unconfigure_snmp_server_user(
            device,
            user_name='u1',
            group_name='g1',
            version='v2c',
            auth_type='sha',
        )
        device.configure.assert_called_once()


class TestConfigureIpSshVersionAcceptsInt(unittest.TestCase):

    def test_int_version_accepted(self):
        device = MagicMock()
        configure_ip_ssh_version(device, version=2)
        device.configure.assert_called_once_with('ip ssh version 2')


if __name__ == '__main__':
    unittest.main()
