from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.apphosting.configure import unconfigure_app_hosting_appid


class TestUnconfigureAppHostingAppid(TestCase):

    def test_unconfigure_app_hosting_appid(self):
        self.device = Mock()
        unconfigure_app_hosting_appid(self.device, 'APP')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no app-hosting appid APP',)
        )
