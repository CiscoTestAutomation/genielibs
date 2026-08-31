import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.snmp.configure import (
    unconfigure_snmp_server_trap,
)


class TestUnconfigureSnmpServerTrap(unittest.TestCase):

    def test_unconfigure_snmp_server_trap(self):
        device = Mock()

        result = unconfigure_snmp_server_trap(
            device,
            'HundredGigE1/0/27',
            '70.70.70.2',
            'traps',
            '3',
            'privuser256256',
            'config',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'no snmp-server trap-source HundredGigE1/0/27',
                'no snmp-server enable traps',
                'no snmp-server host 70.70.70.2 traps version 3 '
                'priv privuser256256 config',
            ]
        )

    def test_unconfigure_snmp_server_inform_with_engine_id(self):
        device = Mock()

        result = unconfigure_snmp_server_trap(
            device,
            'HundredGigE1/0/27',
            '70.70.70.2',
            'informs',
            '3',
            'privuser256256',
            'config',
            '800000090300005056BE0829',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'no snmp-server trap-source HundredGigE1/0/27',
                'no snmp-server enable traps',
                'no snmp-server host 70.70.70.2 informs version 3 '
                'priv privuser256256 config',
                'no snmp-server engineID remote 70.70.70.2 '
                '800000090300005056BE0829',
            ]
        )

    def test_unconfigure_snmp_server_trap_type(self):
        device = Mock()

        result = unconfigure_snmp_server_trap(
            device,
            trap_type='snmp',
            version=None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'no snmp-server enable traps snmp',
            ]
        )

    def test_unconfigure_snmp_server_trap_default(self):
        device = Mock()

        result = unconfigure_snmp_server_trap(
            device,
            version=None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'no snmp-server enable traps',
            ]
        )
