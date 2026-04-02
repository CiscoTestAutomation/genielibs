import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    configure_evpn_l2_instance_bd_association,
)


class TestConfigureEvpnL2InstanceBdAssociation(TestCase):

    def test_configure_evpn_l2_instance_bd_association(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_evpn_l2_instance_bd_association(
            device,
            40,     # bridge-domain
            9,      # evpn-instance
            30012,  # vni
            20012   # ethernet-tag
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate the configuration lines passed to device.configure(...)
        cfg_arg = device.configure.mock_calls[0].args[0]

        # API may pass a list of commands or a multiline string; normalize to list
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('bridge-domain 40', cfg_lines)
        self.assertIn(
            'member evpn-instance 9 vni 30012 ethernet-tag 20012',
            cfg_lines
        )


if __name__ == '__main__':
    unittest.main()