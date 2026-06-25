from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lldp.configure import (
    unconfigure_lldp_interface_only,
)
from unicon.core.errors import SubCommandFailure


class TestUnconfigureLldpInterfaceOnly(TestCase):

    def test_unconfigure_lldp_interface_only_both(self):
        device = Mock()
        result = unconfigure_lldp_interface_only(
            device, 'GigabitEthernet1/0/1', True, True
        )
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet1/0/1',
                'no lldp transmit',
                'no lldp receive',
            ],)
        )

    def test_unconfigure_lldp_interface_only_transmit_only(self):
        device = Mock()
        result = unconfigure_lldp_interface_only(
            device, 'GigabitEthernet1/0/1', True, False
        )
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet1/0/1',
                'no lldp transmit',
            ],)
        )

    def test_unconfigure_lldp_interface_only_receive_only(self):
        device = Mock()
        result = unconfigure_lldp_interface_only(
            device, 'GigabitEthernet1/0/1', False, True
        )
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet1/0/1',
                'no lldp receive',
            ],)
        )

    def test_unconfigure_lldp_interface_only_subcommand_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('failed')
        with self.assertRaises(SubCommandFailure):
            unconfigure_lldp_interface_only(
                device, 'GigabitEthernet1/0/1', True, True
            )
