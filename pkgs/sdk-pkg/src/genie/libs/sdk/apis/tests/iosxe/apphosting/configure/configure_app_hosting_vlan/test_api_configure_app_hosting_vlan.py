from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_vlan
from unittest.mock import Mock


class TestConfigureAppHostingVlan(TestCase):

    def test_configure_app_hosting_vlan(self):
        self.device = Mock()
        result = configure_app_hosting_vlan(self.device, '1keyes', '5')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1keyes', 'vlan 5', 'state active', 'interface vlan 5', 'no shutdown'],)
        )
