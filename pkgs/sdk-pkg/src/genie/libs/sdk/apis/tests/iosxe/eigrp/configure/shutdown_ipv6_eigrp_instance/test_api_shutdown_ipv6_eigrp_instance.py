import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import shutdown_ipv6_eigrp_instance


class TestShutdownIpv6EigrpInstance(TestCase):

    def test_shutdown_ipv6_eigrp_instance(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = shutdown_ipv6_eigrp_instance(device, 1)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('ipv6 router eigrp 1', sent_commands)
        self.assertIn('shutdown', sent_commands)


if __name__ == '__main__':
    unittest.main()