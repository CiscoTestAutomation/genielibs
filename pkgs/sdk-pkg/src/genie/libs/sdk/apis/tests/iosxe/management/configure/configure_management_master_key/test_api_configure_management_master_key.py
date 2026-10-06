from unittest import TestCase
from unittest.mock import ANY, Mock, patch, call
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_master_key
from unicon.eal.dialogs import Dialog


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
        self.assertEqual(
            self.device.configure.call_args.kwargs,
            {'reply': ANY, 'timeout': 300},
        )
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
            self.device.configure.call_args_list[0].kwargs,
            {'reply': ANY, 'timeout': 300},
        )
        self.assertEqual(
            self.device.configure.call_args_list[1],
            call('password encryption aes'),
        )
        self.assertTrue(result)

    def test_dialog_handles_new_and_confirm_key_prompts(self):
        """Regression for CSCwv17868: on platforms (e.g. IE3xxx/IE9xxx) that
        still prompt for 'New key:'/'Confirm key:' despite the key being
        passed inline, the command previously hung until timeout because
        the Dialog had no matching Statement. Verify both prompts are now
        handled with a sendline of the generated key."""
        self.device.configure.return_value = 'R1(config)#'

        configure_management_master_key(self.device)

        reply_dialog = self.device.configure.call_args_list[0].kwargs['reply']
        self.assertIsInstance(reply_dialog, Dialog)
        statements = {statement.pattern: statement for statement in reply_dialog}
        self.assertIn('Old key:', statements)
        self.assertIn('New key:', statements)
        self.assertIn('Confirm key:', statements)

        key = self.device.configure.call_args_list[0][0][0].rsplit(' ', 1)[-1]
        spawn = Mock()
        statements['New key:'].action(spawn, key)
        spawn.sendline.assert_called_once_with(key)

        spawn.reset_mock()
        statements['Confirm key:'].action(spawn, key)
        spawn.sendline.assert_called_once_with(key)
