import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import (
    unconfigure_ipv6_eigrp_router
)


class TestUnconfigureIpv6EigrpRouter(TestCase):

    def test_unconfigure_ipv6_eigrp_router(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_ipv6_eigrp_router(device, '66')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('no ipv6 router eigrp 66', sent_commands)


if __name__ == '__main__':
    unittest.main()