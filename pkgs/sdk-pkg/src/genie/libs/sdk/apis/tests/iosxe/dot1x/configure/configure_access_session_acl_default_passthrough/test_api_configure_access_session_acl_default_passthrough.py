import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_access_session_acl_default_passthrough

class TestConfigureAccessSessionAclDefaultPassthrough(TestCase):

    def test_configure_access_session_acl_default_passthrough(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Simulate device in enable mode

        result = configure_access_session_acl_default_passthrough(device)
        expected_output = None
        self.assertEqual(result, expected_output)

        # Check that the correct command was sent
        self.assertIn(
            'access-session acl default passthrough',
            device.configure.mock_calls[0].args[0]
        )

if __name__ == '__main__':
    unittest.main()