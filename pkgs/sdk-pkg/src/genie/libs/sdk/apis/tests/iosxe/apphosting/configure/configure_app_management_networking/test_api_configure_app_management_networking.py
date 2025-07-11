from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_management_networking


class TestConfigureAppManagementNetworking(TestCase):

    def test_configure_app_management_networking(self):
        self.device = Mock()
        configure_app_management_networking(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid guestshell', 'app-vnic management guest-interface 0'],)
        )
