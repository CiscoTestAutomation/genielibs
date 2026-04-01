import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import unconfigure_eigrp_passive_interface


class TestUnconfigureEigrpPassiveInterface(TestCase):

    def test_unconfigure_eigrp_passive_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_eigrp_passive_interface(device, '1', ['GigabitEthernet0/0/0'])

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('router eigrp 1', sent_commands)
        self.assertIn('no passive-interface GigabitEthernet0/0/0', sent_commands)


if __name__ == '__main__':
    unittest.main()