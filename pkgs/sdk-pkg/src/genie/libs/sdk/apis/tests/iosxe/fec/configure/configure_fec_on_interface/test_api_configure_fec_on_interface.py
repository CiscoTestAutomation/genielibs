import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.fec.configure import (
    configure_fec_on_interface
)


class TestConfigureFecOnInterface(TestCase):

    def test_configure_fec_on_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_fec_on_interface(
            device,
            'TwentyFiveGigE1/1/1',
            'auto'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('interface TwentyFiveGigE1/1/1', sent_commands)
        self.assertIn('fec auto', sent_commands)


if __name__ == '__main__':
    unittest.main()