import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.gdoi.configure import unconfigure_gdoi_group_on_gm


class TestUnconfigureGdoiGroupOnGm(TestCase):

    def test_unconfigure_gdoi_group_on_gm_ipv6(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_gdoi_group_on_gm(device, 'gp_2', True)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate commands
        cfg_arg = device.configure.mock_calls[0].args[0]

        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('no crypto gdoi group ipv6 gp_2', cfg_lines)

    def test_unconfigure_gdoi_group_on_gm_ipv4(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_gdoi_group_on_gm(device, 'gp_1', False)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate commands
        cfg_arg = device.configure.mock_calls[0].args[0]

        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('no crypto gdoi group gp_1', cfg_lines)


if __name__ == '__main__':
    unittest.main()