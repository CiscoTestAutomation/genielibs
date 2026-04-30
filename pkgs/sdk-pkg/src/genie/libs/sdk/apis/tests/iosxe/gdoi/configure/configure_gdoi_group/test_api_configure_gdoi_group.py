import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.gdoi.configure import configure_gdoi_group


class TestConfigureGdoiGroup(TestCase):

    def test_configure_gdoi_group(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_gdoi_group(
            device, 'SUITEBv4', False, 9000, '15.15.15.1', True,
            'aes 256', '14000', '10', '3', 'REKEYRSA', False, '10',
            'SUITEBgcm128', 'SUITEBv4acl', None, False, '20', False,
            '15.15.15.1', False, '245', '16.16.16.1', True, None, 1,
            'IKEV2-PROF1', 121, 'IKEV2-PROF1', True
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for assertions (API may pass list or multiline string)
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('crypto gdoi group SUITEBv4', cfg_lines)
        self.assertIn('identity number 9000', cfg_lines)
        self.assertIn('server address ipv4 15.15.15.1', cfg_lines)
        self.assertIn('client protocol gikev2 IKEV2-PROF1', cfg_lines)
        self.assertIn('server local', cfg_lines)
        self.assertIn('rekey algorithm aes 256', cfg_lines)
        self.assertIn('rekey lifetime seconds 14000', cfg_lines)
        self.assertIn('rekey address ipv4 121', cfg_lines)
        self.assertIn('rekey retransmit 10 number 3', cfg_lines)
        self.assertIn('rekey authentication mypubkey rsa REKEYRSA', cfg_lines)
        self.assertIn('pfs', cfg_lines)
        self.assertIn('gikev2 IKEV2-PROF1', cfg_lines)
        self.assertIn('sa ipsec 10', cfg_lines)
        self.assertIn('profile SUITEBgcm128', cfg_lines)
        self.assertIn('match address ipv4 SUITEBv4acl', cfg_lines)
        self.assertIn('no replay', cfg_lines)
        self.assertIn('no tag', cfg_lines)
        self.assertIn('address ipv4 15.15.15.1', cfg_lines)
        self.assertIn('identifier', cfg_lines)
        self.assertIn('value 1', cfg_lines)


if __name__ == '__main__':
    unittest.main()