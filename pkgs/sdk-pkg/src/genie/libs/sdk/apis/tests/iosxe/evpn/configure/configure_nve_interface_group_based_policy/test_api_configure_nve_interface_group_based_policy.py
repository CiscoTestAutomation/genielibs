import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    configure_nve_interface_group_based_policy,
)


class TestConfigureNveInterfaceGroupBasedPolicy(TestCase):

    def test_configure_nve_interface_group_based_policy(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_nve_interface_group_based_policy(device, '1')
        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate commands passed to device.configure(...)
        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for assertions (API may pass list or multiline string)
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('interface nve 1', cfg_lines)
        self.assertIn('group-based-policy', cfg_lines)


if __name__ == '__main__':
    unittest.main()