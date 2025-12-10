from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_credentials
from unittest.mock import Mock


class TestConfigureManagementCredentials(TestCase):

    def test_configure_management_credentials(self):
        self.device = Mock()
        result = configure_management_credentials(self.device, None, 'test-user', 'cisco@123')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['aaa new-model',
              'aaa authentication login default local',
              'aaa authorization exec default local',
              'no username test-user password',
              'username test-user secret cisco@123',
              'username test-user privilege 15'],)
        )
