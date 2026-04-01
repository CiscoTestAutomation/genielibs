import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import unconfigure_eigrp_router_configs


class TestUnconfigureEigrpRouterConfigs(TestCase):

    def test_unconfigure_eigrp_router_configs(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_eigrp_router_configs(device, 100, 12, False)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('router eigrp 100', sent_commands)
        self.assertIn('no maximum-paths', sent_commands)
        self.assertNotIn('no auto-summary', sent_commands)

    def test_unconfigure_eigrp_router_configs_1(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_eigrp_router_configs(device, 100, 9, False)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('router eigrp 100', sent_commands)
        self.assertIn('no maximum-paths', sent_commands)
        self.assertNotIn('no auto-summary', sent_commands)

    def test_unconfigure_eigrp_router_configs_2(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_eigrp_router_configs(device, 100, 24, True)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('router eigrp 100', sent_commands)
        self.assertIn('no maximum-paths', sent_commands)
        self.assertIn('no auto-summary', sent_commands)


if __name__ == '__main__':
    unittest.main()