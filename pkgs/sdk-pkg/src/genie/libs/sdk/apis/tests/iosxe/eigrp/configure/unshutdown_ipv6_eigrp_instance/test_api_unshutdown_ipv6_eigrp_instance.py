import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import (
    unshutdown_ipv6_eigrp_instance
)


class TestUnshutdownIpv6EigrpInstance(TestCase):

    def test_unshutdown_ipv6_eigrp_instance(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unshutdown_ipv6_eigrp_instance(device, 1)

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('ipv6 router eigrp 1', sent_commands)
        self.assertIn('no shutdown', sent_commands)


if __name__ == '__main__':
    unittest.main()