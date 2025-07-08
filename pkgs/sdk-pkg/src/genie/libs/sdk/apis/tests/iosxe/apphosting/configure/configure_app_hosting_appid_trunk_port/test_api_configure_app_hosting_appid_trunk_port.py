from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_appid_trunk_port


class TestConfigureAppHostingAppidTrunkPort(TestCase):

    def test_configure_app_hosting_appid_trunk_port(self):
        self.device = Mock()
        configure_app_hosting_appid_trunk_port(self.device, '1key', 'AppGigabitEthernet', 2, 'trunk', None, 14, '172.15.0.1', '255.255.255.0', '172.15.0.255', True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key', 'app-vnic AppGigabitEthernet port 2 trunk', 'vlan 14 guest-interface 0',
              'guest-ipaddress 172.15.0.1 netmask 255.255.255.0', 'app-default-gateway 172.15.0.255 guest-interface 0', 'start'] ,)
        )

    def test_configure_app_hosting_appid_trunk_port_1(self):
        self.device = Mock()
        configure_app_hosting_appid_trunk_port(self.device, '1key1', 'management', None, None, 0, None, None, None, '172.15.0.255', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key1', 'app-vnic management guest-interface 0',
              'app-default-gateway 172.15.0.255 guest-interface 0'] ,)
        )

    def test_configure_app_hosting_appid_trunk_port_2(self):
        self.device = Mock()
        configure_app_hosting_appid_trunk_port(self.device, '1key2', 'AppGigabitEthernet', 2, 'trunk', None, 14, '172.15.0.1', '255.255.255.0', None, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key2', 'app-vnic AppGigabitEthernet port 2 trunk',
              'vlan 14 guest-interface 0', 'guest-ipaddress 172.15.0.1 netmask 255.255.255.0', 'start'] ,)
        )
