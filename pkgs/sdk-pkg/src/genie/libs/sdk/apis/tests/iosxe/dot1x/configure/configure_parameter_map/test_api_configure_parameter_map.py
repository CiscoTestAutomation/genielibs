import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_parameter_map


class TestConfigureParameterMap(TestCase):

    def test_configure_parameter_map(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Device in enable mode

        result = configure_parameter_map(
            device,
            False, True, 'banner', 'c banner-text c', 'c banner-title c',
            True, True, True, True, 'html', 'logindevice', None, 'success',
            True, 10, 'append client-mac tag vis', 11, True, 60, 'consent',
            85, True, True, 'vis', '10.10.10.10', '10:10:10::1',
            '1.1.1.1', '20:20:20::1', 10, True, 'vis', None, True
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate the commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        # If API sends a multiline string, this still works because we use assertIn
        self.assertIn('parameter-map type webauth global', sent_commands)
        self.assertIn('banner file banner', sent_commands)
        self.assertIn('banner text c banner-text c', sent_commands)
        self.assertIn('banner title c banner-title c', sent_commands)
        self.assertIn('captive-bypass-portal', sent_commands)
        self.assertIn('cisco-logo-disable', sent_commands)
        self.assertIn('consent email', sent_commands)
        self.assertIn('custom-page failure device html', sent_commands)
        self.assertIn('custom-page failure device success', sent_commands)
        self.assertIn('custom-page login device logindevice', sent_commands)
        self.assertIn('redirect append client-mac tag vis', sent_commands)
        self.assertIn('timeout init-state sec 60', sent_commands)
        self.assertIn('http port 85', sent_commands)
        self.assertIn('trustpoint vis', sent_commands)
        self.assertIn('virtual-ip ipv4 10.10.10.10', sent_commands)
        self.assertIn('virtual-ip ipv6 10:10:10::1', sent_commands)
        self.assertIn('watch-list add-item ipv4 1.1.1.1', sent_commands)
        self.assertIn('watch-list add-item ipv6 20:20:20::1', sent_commands)
        self.assertIn('watch-list dynamic-expiry-timeout 10', sent_commands)
        self.assertIn('watch-list enabled', sent_commands)
        self.assertIn('webauth-bypass-intercept None', sent_commands)
        self.assertIn('webauth-http-enable', sent_commands)


if __name__ == '__main__':
    unittest.main()