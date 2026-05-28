import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_key_config_key_newpass_oldpass


class TestConfigureKeyConfigKeyNewpassOldpass(unittest.TestCase):

    def test_configure_key_config_key_newpass_oldpass(self):
        device = Mock()

        result = configure_key_config_key_newpass_oldpass(device, 'test4567', 'cisco123')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('key config-key newpass test4567 oldpass cisco123',)
        )