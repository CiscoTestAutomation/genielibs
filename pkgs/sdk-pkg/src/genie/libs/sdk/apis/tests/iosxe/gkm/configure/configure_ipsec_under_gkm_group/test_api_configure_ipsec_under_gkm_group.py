import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.gkm.configure import configure_ipsec_under_gkm_group


class TestConfigureIpsecUnderGkmGroup(TestCase):

    def test_configure_ipsec_under_gkm_group(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_ipsec_under_gkm_group(
            device,
            'v4-cust-gdoi1000',
            True,
            '1',
            'cust-ipsec',
            'ks-max-acl-replace(permit-any)',
            None,
            True,
            '20',
            False
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
        self.assertIn('server local', cfg_lines)
        self.assertIn('sa ipsec 1', cfg_lines)
        self.assertIn('profile cust-ipsec', cfg_lines)
        self.assertIn('match address ipv4 ks-max-acl-replace(permit-any)', cfg_lines)
        self.assertIn('replay time window-size 20', cfg_lines)


if __name__ == '__main__':
    unittest.main()