import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.snmp.configure import (
    unconfigure_snmp_server_user,
)


class TestUnconfigureSnmpServerUser(unittest.TestCase):

    def test_unconfigure_snmp_server_user_with_ipv6_acl(self):
        device = Mock()

        result = unconfigure_snmp_server_user(
            device,
            'privuser256256',
            'privgrp',
            'v3',
            'sha-2',
            '256',
            'cisco256',
            'aes',
            '256',
            'cisco256',
            acl_type='ipv6',
            acl_name='nameacl',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server user privuser256256 privgrp v3 '
            'auth sha-2 256 cisco256 priv aes 256 cisco256 '
            'access ipv6 nameacl nameacl'
        )

    def test_unconfigure_snmp_server_user_with_auth_and_priv(self):
        device = Mock()

        result = unconfigure_snmp_server_user(
            device,
            'privuser256256',
            'privgrp',
            'v3',
            'sha-2',
            '256',
            'cisco256',
            'aes',
            '256',
            'cisco256',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server user privuser256256 privgrp v3 '
            'auth sha-2 256 cisco256 priv aes 256 cisco256'
        )

    def test_unconfigure_snmp_server_user_with_auth(self):
        device = Mock()

        result = unconfigure_snmp_server_user(
            device,
            'privuser256256',
            'privgrp',
            'v3',
            'sha-2',
            '256',
            'cisco256',
            priv_method=None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server user privuser256256 privgrp v3 '
            'auth sha-2 256 cisco256'
        )

    def test_unconfigure_snmp_server_user_default(self):
        device = Mock()

        result = unconfigure_snmp_server_user(
            device,
            'privuser256256',
            'privgrp',
            'v3',
            auth_type=None,
            priv_method=None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server user privuser256256 privgrp v3'
        )
