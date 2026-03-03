import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    unconfigure_access_session_acl_default_passthrough
)


class TestUnconfigureAccessSessionAclDefaultPassthrough(TestCase):

    def test_unconfigure_access_session_acl_default_passthrough(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_access_session_acl_default_passthrough(device)

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'no access-session acl default passthrough',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()