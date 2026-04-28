from unittest import TestCase
from unittest.mock import Mock, patch, call
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_master_key


class TestConfigureManagementSecurityCheck(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'R1'

    def test_master_key_missing_configures_key(self):
        """When 'config terminal' output contains 'master key', the API
        must configure the key and return True."""
        self.device.execute.return_value = (
            '% WARNING: The master key is not configured.\n'
            'Configure the master key by using the following command: '
            '"key config-key password-encrypt <encryption-key>"\n'
            'R1(config)#'
        )

        result = configure_management_master_key(self.device)

        # execute called once with 'config terminal'
        self.device.execute.assert_called_once_with(
            'config terminal', allow_state_change=True
        )

        # configure called once with the key commands
        self.device.configure.assert_called_once()
        configure_args = self.device.configure.call_args[0][0]
        self.assertEqual(len(configure_args), 2)
        self.assertTrue(configure_args[0].startswith('key config-key password-encrypt '))
        self.assertEqual(configure_args[1], 'password encryption aes')
        self.assertTrue(result)

