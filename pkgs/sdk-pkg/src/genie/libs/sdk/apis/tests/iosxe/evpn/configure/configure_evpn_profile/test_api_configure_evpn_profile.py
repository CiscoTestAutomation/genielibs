import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import configure_evpn_profile


class TestConfigureEvpnProfile(TestCase):

    def test_configure_evpn_profile(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_evpn_profile(
            device,
            'evpn_va1',
            'vlan-aware',
            1,
            50000,
            'auto-vni',
            'vxlan'
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

        self.assertIn('l2vpn evpn profile evpn_va1 vlan-aware', cfg_lines)
        self.assertIn('evi-id 1', cfg_lines)
        self.assertIn('l2vni-base 50000', cfg_lines)
        self.assertIn('ethernet-tag auto-vni', cfg_lines)
        self.assertIn('encapsulation vxlan', cfg_lines)


if __name__ == '__main__':
    unittest.main()