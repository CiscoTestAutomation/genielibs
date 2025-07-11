from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_appid_iperf_from_vlan


class TestConfigureAppHostingAppidIperfFromVlan(TestCase):

    def test_configure_app_hosting_appid_iperf_from_vlan(self):
        self.device = Mock()
        configure_app_hosting_appid_iperf_from_vlan(self.device, 1, '15')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid iperf','app-vnic AppGigabitEthernet port 1 trunk',
              'Vlan 15 guest-interface 0','start'] ,)
        )
