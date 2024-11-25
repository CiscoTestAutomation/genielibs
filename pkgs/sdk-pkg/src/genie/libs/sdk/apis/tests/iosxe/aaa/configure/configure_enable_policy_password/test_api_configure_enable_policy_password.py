import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_enable_policy_password


class TestConfigureEnablePolicyPassword(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_enable_policy_password(self):
        self.device.configure.side_effect = """
enable common-criteria-policy enable_test password 0 Test12
WARNING: Configured enable password CLI with weak encryption type 0 will be deprecated in future. Hence please migrate to enable secret CLI which accomplishes same functionality as enable password CLI and which also supports strong irreversible encryption type 9
        """
        configure_enable_policy_password(
            device=self.device, password='Test12',
            policy_name='enable_test', password_type=0)
        self.device.configure.assert_called_once_with(
            'enable common-criteria-policy enable_test password 0 Test12')
