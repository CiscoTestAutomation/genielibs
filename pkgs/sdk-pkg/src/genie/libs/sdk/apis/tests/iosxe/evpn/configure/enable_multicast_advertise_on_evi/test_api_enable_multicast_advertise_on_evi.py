import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import enable_multicast_advertise_on_evi


class TestEnableMulticastAdvertiseOnEvi(TestCase):

    def test_enable_multicast_advertise_on_evi(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = enable_multicast_advertise_on_evi(device, 10, 'vlan-based')
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

        self.assertIn('l2vpn evpn instance 10 vlan-based', cfg_lines)
        self.assertIn('multicast advertise enable', cfg_lines)


if __name__ == '__main__':
    unittest.main()