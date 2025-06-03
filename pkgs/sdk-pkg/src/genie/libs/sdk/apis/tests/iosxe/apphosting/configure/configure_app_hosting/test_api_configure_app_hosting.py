from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting
from unittest.mock import Mock


class TestConfigureAppHosting(TestCase):

    def test_configure_app_hosting(self):
        self.device = Mock()
        result = configure_app_hosting(self.device, '1keyes', '14', '14.0.0.13', '255.255.255.0', '14.0.0.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1keyes', 'app-vnic AppGigabitEthernet trunk', 'vlan 14 guest-interface 0', 'guest-ipaddress 14.0.0.13 netmask 255.255.255.0', 'app-default-gateway 14.0.0.1 guest-interface 0'],)
        )
