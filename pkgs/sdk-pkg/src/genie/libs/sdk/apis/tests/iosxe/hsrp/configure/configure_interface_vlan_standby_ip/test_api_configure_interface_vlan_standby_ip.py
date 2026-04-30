import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.hsrp.configure import configure_interface_vlan_standby_ip


class TestConfigureInterfaceVlanStandbyIp(TestCase):

    def test_configure_interface_vlan_standby_ip(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_interface_vlan_standby_ip(
            device,
            '10',
            '0',
            '10.1.0.3'
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

        self.assertIn('interface vlan 10', cfg_lines)
        self.assertIn('standby 0 ip 10.1.0.3', cfg_lines)


if __name__ == '__main__':
    unittest.main()