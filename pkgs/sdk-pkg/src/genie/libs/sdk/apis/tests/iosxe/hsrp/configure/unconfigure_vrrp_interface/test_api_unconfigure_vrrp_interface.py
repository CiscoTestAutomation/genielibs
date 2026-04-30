import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.hsrp.configure import unconfigure_vrrp_interface


class TestUnconfigureVrrpInterface(TestCase):

    def test_unconfigure_vrrp_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_vrrp_interface(
            device,
            'vlan 11',
            '1',
            'ipv4'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate commands passed to device.configure(...)
        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for assertions
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('interface vlan 11', cfg_lines)
        self.assertIn('no vrrp 1 address-family ipv4', cfg_lines)


if __name__ == '__main__':
    unittest.main()