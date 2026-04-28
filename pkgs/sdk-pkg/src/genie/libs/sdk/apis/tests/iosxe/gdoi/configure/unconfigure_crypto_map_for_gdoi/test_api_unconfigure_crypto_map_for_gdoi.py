import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.gdoi.configure import unconfigure_crypto_map_for_gdoi


class TestUnconfigureCryptoMapForGdoi(TestCase):

    def test_unconfigure_crypto_map_for_gdoi(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_crypto_map_for_gdoi(device, 'test_map_ipv6', '12', True)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        cfg_arg = device.configure.mock_calls[0].args[0]

        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('no crypto map ipv6 test_map_ipv6 12 gdoi', cfg_lines)

    def test_unconfigure_crypto_map_for_gdoi_1(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_crypto_map_for_gdoi(device, 'test_map_ipv4', '10', False)

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        cfg_arg = device.configure.mock_calls[0].args[0]

        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('no crypto map test_map_ipv4 10 gdoi', cfg_lines)


if __name__ == '__main__':
    unittest.main()