from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_custom_profile
from unittest.mock import Mock


class TestConfigureAppHostingCustomProfile(TestCase):

    def test_configure_app_hosting_custom_profile(self):
        self.device = Mock()
        result = configure_app_hosting_custom_profile(self.device, '1keyes', '1850', '500', '200', '14.0.0.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1keyes', 'app-resource profile custom', 'cpu 1850', 'memory 500', 'persist-disk 200', 'name-server0 14.0.0.1', 'start'],)
        )
