from unittest import TestCase
from unittest.mock import Mock, patch, call
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_master_key


class TestConfigureManagementSecurityCheck(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'R1'

    def test_key_exists_old_key_prompt(self):
        """When device prompts 'Old key:', the key is already
        present. The API must send Ctrl-C to abort and return False."""
        # configure: key command returns Old key prompt (aborted by dialog)
        self.device.configure.return_value = (
            'Old key: %% Failed to set new key\nR1(config)#'
        )

        result = configure_management_master_key(self.device)

        # configure called once with key command + dialog
        self.device.configure.assert_called_once()
        first_arg = self.device.configure.call_args[0][0]
        self.assertTrue(first_arg.startswith('key config-key password-encrypt '))
        self.assertFalse(result)

    def test_key_not_exists_configures_both(self):
        """When no 'Old key:' prompt, the key is newly set.
        API must then configure 'password encryption aes' and return True."""
        # configure: first call (key command) succeeds, second call (aes)
        self.device.configure.side_effect = [
            'R1(config)#',
            'R1(config)#',
        ]

        result = configure_management_master_key(self.device)

        # configure called twice: key command, then password encryption aes
        self.assertEqual(self.device.configure.call_count, 2)
        first_arg = self.device.configure.call_args_list[0][0][0]
        self.assertTrue(first_arg.startswith('key config-key password-encrypt '))
        self.assertEqual(
            self.device.configure.call_args_list[1],
            call('password encryption aes'),
        )
        self.assertTrue(result)

