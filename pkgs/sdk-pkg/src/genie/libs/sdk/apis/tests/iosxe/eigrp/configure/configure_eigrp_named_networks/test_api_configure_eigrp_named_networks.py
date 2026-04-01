import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import (
    configure_eigrp_named_networks
)


class TestConfigureEigrpNamedNetworks(TestCase):

    def test_configure_eigrp_named_networks(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_eigrp_named_networks(
            device,
            100,          # as_number
            None,         # vrf
            None,         # address_family
            None,         # autonomous_system
            None,         # named_mode
            None,         # address_family_mode
            '',           # interface
            '',           # network
            '3.4.5.6'     # router_id
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'router eigrp 100',
            sent_commands
        )
        self.assertIn(
            'eigrp router-id 3.4.5.6',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()