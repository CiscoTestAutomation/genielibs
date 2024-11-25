import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.verify import verify_login_credentials_enable_password


class TestVerifyLoginCredentialsEnablePassword(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_verify_login_credentials_enable_password(self):
        self.device.execute.side_effect = ['', 'Password:']
        result = verify_login_credentials_enable_password(
            self.device, 'dnac', 'cisco123', True, 'dnac1', '15')
        self.assertIn(
            'exit',
            self.device.execute.call_args_list[0][0]
        )
        self.assertIn(
            'enable 15',
            self.device.execute.call_args_list[1][0]
        )
        self.assertEqual(result, True)
