import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import (
    configure_eigrp_redistribute_bgp
)


class TestConfigureEigrpRedistributeBgp(TestCase):

    def test_configure_eigrp_redistribute_bgp_ipv4(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_eigrp_redistribute_bgp(
            device,
            6,      # eigrp_as
            3,      # bgp_as
            False   # ipv6
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]
        self.assertIn('router eigrp 6', sent_commands)
        self.assertIn('redistribute bgp 3', sent_commands)

    def test_configure_eigrp_redistribute_bgp_ipv6(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_eigrp_redistribute_bgp(
            device,
            8,     # eigrp_as
            3,     # bgp_as
            True   # ipv6
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]
        self.assertIn('ipv6 router eigrp 8', sent_commands)
        self.assertIn('redistribute bgp 3', sent_commands)


if __name__ == '__main__':
    unittest.main()