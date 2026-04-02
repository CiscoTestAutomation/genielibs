import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    configure_evpn_l2_instance_vlan_association,
)


class TestConfigureEvpnL2InstanceVlanAssociation(TestCase):

    def test_configure_evpn_l2_instance_vlan_association(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_evpn_l2_instance_vlan_association(
            device,
            '10',     # vlan
            '10',     # evpn-instance
            '60010'   # vni
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate commands passed to device.configure(...)
        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for easy assertions
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('vlan configuration 10', cfg_lines)

        # Match the command as shown in mock output (note the double space after 'evpn-instance')
        self.assertIn('member evpn-instance  10 vni 60010', cfg_lines)


if __name__ == '__main__':
    unittest.main()