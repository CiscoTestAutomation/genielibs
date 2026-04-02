import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_vfi_context_evpn
)


class TestUnconfigureVfiContextEvpn(TestCase):

    def test_unconfigure_vfi_context_evpn(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        # Simulate device CLI output shown in mock data (non-fatal "does not exist")
        device.configure.return_value = (
            "no l2vpn vfi context VFI201\n"
            "% VFI VFI201 does not exist"
        )

        result = unconfigure_vfi_context_evpn(device, 'VFI201')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]
        self.assertIn('no l2vpn vfi context VFI201', sent_commands)


if __name__ == '__main__':
    unittest.main()