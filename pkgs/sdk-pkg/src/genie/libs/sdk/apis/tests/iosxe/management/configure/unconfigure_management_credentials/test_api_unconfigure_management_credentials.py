from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import unconfigure_management_credentials
from unittest.mock import Mock


class TestUnconfigureManagementCredentials(TestCase):

    def test_unconfigure_management_credentials(self):
        self.device = Mock()
        result = unconfigure_management_credentials(self.device, None, 'test-user', 'cisco@123')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no aaa authentication login default local',
            'no aaa authorization exec default local',
            f'no username test-user',
            'no aaa new-model'],)
        )

