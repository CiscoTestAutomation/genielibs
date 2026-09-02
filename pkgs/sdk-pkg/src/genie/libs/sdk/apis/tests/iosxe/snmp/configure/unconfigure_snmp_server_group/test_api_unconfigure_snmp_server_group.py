import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.snmp.configure import (
    unconfigure_snmp_server_group,
)


class TestUnconfigureSnmpServerGroup(unittest.TestCase):

    def test_unconfigure_snmp_server_group(self):
        device = Mock()

        result = unconfigure_snmp_server_group(
            device,
            'snmp_group',
            'v3',
            'auth',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server group snmp_group v3 auth'
        )

    def test_unconfigure_snmp_server_group_with_ipv6_acl(self):
        device = Mock()

        result = unconfigure_snmp_server_group(
            device,
            'snmp_group',
            'v3',
            'auth',
            acl_name='useracl',
            acl_type='ipv6',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server group snmp_group v3 auth '
            'access ipv6 useracl useracl'
        )

    def test_unconfigure_snmp_server_group_with_read_view_and_ipv6_acl(self):
        device = Mock()

        result = unconfigure_snmp_server_group(
            device,
            'snmp_group',
            'v3',
            'auth',
            mode='read',
            acl_name='useracl',
            view_name='readwrite',
            acl_type='ipv6',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server group snmp_group v3 auth read readwrite '
            'access ipv6 useracl useracl'
        )

    def test_unconfigure_snmp_server_group_with_context(self):
        device = Mock()

        result = unconfigure_snmp_server_group(
            device,
            'snmp_group',
            'v3',
            'auth',
            context_name='context',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server group snmp_group v3 auth context context'
        )

    def test_unconfigure_snmp_server_group_with_match_type(self):
        device = Mock()

        result = unconfigure_snmp_server_group(
            device,
            'snmp_group',
            'v3',
            'auth',
            match_type='exact',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server group snmp_group v3 auth match exact'
        )

    def test_unconfigure_snmp_server_group_with_notify_and_acl(self):
        device = Mock()

        result = unconfigure_snmp_server_group(
            device,
            'snmp_group',
            'v3',
            'auth',
            acl_name='useracl',
            notify_name='notify',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server group snmp_group v3 auth notify notify '
            'access useracl'
        )
