import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import unconfigure_eigrp_router


class TestUnconfigureEigrpRouter(TestCase):

    def test_unconfigure_eigrp_router(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_eigrp_router(device, '100')

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('no router eigrp 100', sent_commands)


if __name__ == '__main__':
    unittest.main()