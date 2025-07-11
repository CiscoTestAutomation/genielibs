from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_resource_profile


class TestConfigureAppHostingResourceProfile(TestCase):

    def test_configure_app_hosting_resource_profile(self):
        self.device = Mock()
        configure_app_hosting_resource_profile(self.device, '1key', 'custom', 40, 30, 4000, 5666, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key', 'app-resource profile custom', 'cpu 40',
              'cpu-percent 30', 'memory 4000', 'vcpu 5666', 'start'] ,)
        )

    def test_configure_app_hosting_resource_profile_1(self):
        self.device = Mock()
        configure_app_hosting_resource_profile(self.device, '1key1', 'custom', 40, None, 4000, 5666, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key1', 'app-resource profile custom', 'cpu 40', 'memory 4000', 'vcpu 5666'] ,)
        )

    def test_configure_app_hosting_resource_profile_2(self):
        self.device = Mock()
        configure_app_hosting_resource_profile(self.device, '1key', 'custom', 40, None, None, 5666, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key', 'app-resource profile custom', 'cpu 40', 'vcpu 5666'] ,)
        )


