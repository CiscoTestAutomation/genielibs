import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_parameter_map_subscriber


class TestConfigureParameterMapSubscriber(TestCase):

    def test_configure_parameter_map_subscriber(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Device in enable mode

        result = configure_parameter_map_subscriber(
            device,
            'Identity',
            10,
            'eq',
            'device-type',
            'device1',
            10,
            'interface-template',
            'Identity'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate the commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        # Normalize (handles list entries like "...\n")
        normalized = [cmd.strip() for cmd in sent_commands]

        self.assertIn(
            'parameter-map type subscriber attribute-to-service Identity',
            normalized
        )
        self.assertIn('10 map device-type eq device1', normalized)
        self.assertIn('10 interface-template Identity', normalized)


if __name__ == '__main__':
    unittest.main()