import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import configure_vfi_context_evpn


class TestConfigureVfiContextEvpn(TestCase):

    def test_configure_vfi_context_evpn(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_vfi_context_evpn(
            device,
            'VFI201',
            '201',
            'ethernet-segment',
            '201',
            '172.16.255.5',
            '201',
            'encapsulation',
            'mpls',
            None,
            None,
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

        self.assertIn('l2vpn vfi context VFI201', cfg_lines)
        self.assertIn('vpn id 201', cfg_lines)
        self.assertIn('evpn ethernet-segment 201', cfg_lines)
        self.assertIn('member 172.16.255.5 201 encapsulation mpls', cfg_lines)


if __name__ == '__main__':
    unittest.main()