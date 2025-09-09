from unittest import TestCase
from genie.libs.sdk.apis.iosxe.routing.configure import configure_ip_route_cache_on_interface
from unittest.mock import Mock


class TestConfigureIpRouteCacheOnInterface(TestCase):

    def test_configure_ip_route_cache_on_interface(self):
        self.device = Mock()
        configure_ip_route_cache_on_interface(self.device, 'GigabitEthernet0/1/1', cef=False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/1/1', 'ip route-cache'],)
        )


    def test_configure_ip_route_cache_on_interface_with_cef(self):
        self.device = Mock()
        configure_ip_route_cache_on_interface(self.device, 'GigabitEthernet0/1/1', cef=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/1/1', 'ip route-cache cef'],)
        )
