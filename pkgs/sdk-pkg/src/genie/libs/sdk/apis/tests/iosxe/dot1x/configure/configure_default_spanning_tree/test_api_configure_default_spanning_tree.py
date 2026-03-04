import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_default_spanning_tree
)


class TestConfigureDefaultSpanningTree(TestCase):

    def test_configure_default_spanning_tree(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_default_spanning_tree(
            device,
            'mode'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'default spanning-tree mode mode',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()