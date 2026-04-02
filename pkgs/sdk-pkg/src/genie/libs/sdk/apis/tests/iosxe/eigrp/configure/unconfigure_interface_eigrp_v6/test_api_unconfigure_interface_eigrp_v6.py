import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import (
    unconfigure_interface_eigrp_v6
)


class TestUnconfigureInterfaceEigrpV6(TestCase):

    def test_unconfigure_interface_eigrp_v6(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_interface_eigrp_v6(
            device,
            ['TenGigabitEthernet1/0/3'],
            '66'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        # Verify the interface entry and the unconfiguration command
        self.assertIn('interface TenGigabitEthernet1/0/3', sent_commands)
        self.assertIn('no ipv6 eigrp 66', sent_commands)


if __name__ == '__main__':
    unittest.main()