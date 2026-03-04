import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_dot1x_cred_profile
)


class TestConfigureDot1xCredProfile(TestCase):

    def test_configure_dot1x_cred_profile(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume enable mode

        result = configure_dot1x_cred_profile(
            device,
            'dot1x_prof',
            'dotxuser',
            ']hc[ZbOgC[X[_JV_cbCgIUbSAGK',
            'ENCRYPTED'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('dot1x credentials dot1x_prof', sent_commands)
        self.assertIn('username dotxuser', sent_commands)
        self.assertIn(
            'password 6 ]hc[ZbOgC[X[_JV_cbCgIUbSAGK',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()