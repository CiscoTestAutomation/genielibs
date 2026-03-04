import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1x.configure import clear_access_session_mac

class TestClearAccessSessionMac(TestCase):

    def test_clear_access_session_mac(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Simulate device in enable mode

        result = clear_access_session_mac(device, '0000.0000.0001')
        expected_output = None
        self.assertEqual(result, expected_output)

        # Check that the correct command was sent
        self.assertIn(
            'clear access-session mac 0000.0000.0001',
            device.execute.mock_calls[0].args[0]
        )

if __name__ == '__main__':
    unittest.main()