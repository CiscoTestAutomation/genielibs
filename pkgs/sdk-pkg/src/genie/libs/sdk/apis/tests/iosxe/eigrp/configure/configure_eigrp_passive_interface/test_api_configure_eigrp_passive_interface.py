import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import (
    configure_eigrp_passive_interface
)


class TestConfigureEigrpPassiveInterface(TestCase):

    def test_configure_eigrp_passive_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_eigrp_passive_interface(
            device,
            '1',
            ['GigabitEthernet0/0/0']
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('router eigrp 1', sent_commands)
        self.assertIn('passive-interface GigabitEthernet0/0/0', sent_commands)


if __name__ == '__main__':
    unittest.main()