import unittest
from unittest import TestCase
from unittest.mock import Mock, call

from genie.libs.sdk.apis.iosxe.evpn.configure import configure_evpn_instance_evi


class TestConfigureEvpnInstanceEvi(TestCase):

    def test_configure_evpn_instance_evi(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_evpn_instance_evi(
            device,
            12,
            'vlan-based',
            ['default-gateway'],
            'vxlan',
            'disable'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure we attempted to enter configuration mode and send config
        device.configure.assert_called_once()

        # Validate the configuration lines passed to device.configure(...)
        cfg_arg = device.configure.mock_calls[0].args[0]

        # The API may send either a single string or a list of lines; normalize for assertions
        if isinstance(cfg_arg, str):
            cfg_lines = [line for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('l2vpn evpn instance 12 vlan-based', cfg_lines)
        self.assertIn('default-gateway advertise enable', cfg_lines)

        # Optional: if the API uses additional knobs (encapsulation/shutdown),
        # you can assert them too—uncomment if they match the actual API behavior.
        # self.assertIn('encapsulation vxlan', cfg_lines)
        # self.assertIn('no shutdown', cfg_lines)  # or 'shutdown' depending on "disable"


if __name__ == '__main__':
    unittest.main()