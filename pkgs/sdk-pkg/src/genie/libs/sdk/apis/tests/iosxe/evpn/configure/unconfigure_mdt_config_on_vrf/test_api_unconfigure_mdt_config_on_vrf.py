import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_mdt_config_on_vrf
)


class TestUnconfigureMdtConfigOnVrf(TestCase):

    def test_unconfigure_mdt_config_on_vrf(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_mdt_config_on_vrf(
            device,
            'red',
            'ipv4',
            'overlay',
            'use-bgp',
            'spt-only'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('vrf definition red', sent_commands)
        self.assertIn('address-family ipv4', sent_commands)
        self.assertIn('no mdt overlay use-bgp spt-only', sent_commands)


if __name__ == '__main__':
    unittest.main()