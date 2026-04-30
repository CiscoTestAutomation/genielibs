import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.gdoi.configure import configure_crypto_map_for_gdoi


class TestConfigureCryptoMapForGdoi(TestCase):

    def test_configure_crypto_map_for_gdoi(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_crypto_map_for_gdoi(
            device, 'test_map_ipv6', '12', 'gp_2',
            'This is a ipv6 crypto map', True
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        cfg_arg = device.configure.mock_calls[0].args[0]

        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('crypto map ipv6 test_map_ipv6 12 gdoi', cfg_lines)
        self.assertIn('set group gp_2', cfg_lines)
        self.assertIn('description This is a ipv6 crypto map', cfg_lines)

    def test_configure_crypto_map_for_gdoi_1(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_crypto_map_for_gdoi(
            device, 'test_map_ipv4', '10', 'gp_1',
            'This is a ipv4 crypto map', False
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        cfg_arg = device.configure.mock_calls[0].args[0]

        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('crypto map test_map_ipv4 10  gdoi', cfg_lines)
        self.assertIn('set group gp_1', cfg_lines)
        self.assertIn('description This is a ipv4 crypto map', cfg_lines)


if __name__ == '__main__':
    unittest.main()