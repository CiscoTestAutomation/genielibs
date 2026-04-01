import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import configure_nve_interface


class TestConfigureNveInterface(TestCase):

    def test_configure_nve_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_nve_interface(
            device,
            '1',
            'loopback1',
            'bgp',
            '11500',
            'static',
            '226.0.0.1',
            'True',
            'red'
        )

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
        self.assertIn('source-interface loopback1', cfg_lines)
        self.assertIn('host-reachability protocol bgp', cfg_lines)
        self.assertIn('member vni 11500 mcast-group 226.0.0.1', cfg_lines)


if __name__ == '__main__':
    unittest.main()