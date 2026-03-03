import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_access_session_mac_move

class TestConfigureAccessSessionMacMove(TestCase):

    def test_configure_access_session_mac_move(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Simulate enable mode

        result = configure_access_session_mac_move(device, 'mac-move', 'deny-uncontrolled')
        expected_output = None
        self.assertEqual(result, expected_output)

        # Check that the correct command was sent
        self.assertIn(
            'access-session mac-move deny-uncontrolled',
            device.configure.mock_calls[0].args[0]
        )

if __name__ == '__main__':
    unittest.main()