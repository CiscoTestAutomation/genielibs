import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.gkm.configure import configure_gkm_group_identity_number


class TestConfigureGkmGroupIdentityNumber(TestCase):

    def test_configure_gkm_group_identity_number(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gkm_group_identity_number(
            device,
            'v4-cust-gdoi1000',
            '1000'
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

        self.assertIn('crypto gkm group v4-cust-gdoi1000', cfg_lines)
        self.assertIn('identity number 1000', cfg_lines)


if __name__ == '__main__':
    unittest.main()