import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1x.configure import clear_access_session

class TestClearAccessSession(TestCase):

    def test_clear_access_session(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Simulate enable mode

        result = clear_access_session(device, 'HundredGigE1/0/23')
        expected_output = None
        self.assertEqual(result, expected_output)

        # Check that the expected command was sent
        self.assertIn(
            'clear access-session interface HundredGigE1/0/23',
            device.execute.mock_calls[0].args[0]
        )

if __name__ == '__main__':
    unittest.main()