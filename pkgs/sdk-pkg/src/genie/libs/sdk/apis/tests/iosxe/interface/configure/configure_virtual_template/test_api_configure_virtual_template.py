from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_virtual_template
from unittest.mock import Mock


class TestConfigureVirtualTemplate(TestCase):

    def test_configure_virtual_template(self):
        self.device = Mock()
        result = configure_virtual_template(self.device, 100, 'loopback1', True, 'chap', True, True, 1400, '30', '1500', '1460', True, True, 'v4_pool', 'v6_pool', True, 'explicit-null')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Virtual-Template 100', 'ip unnumbered loopback1', 'ppp authentication chap', 'ip tcp adjust-mss 1400', 'load-interval 30', 'mtu 1500', 'ipv6 mtu 1460', 'no ip redirects', 'no peer default ip address', 'peer default ip address pool v4_pool', 'peer default ipv6 pool v6_pool', 'mpls ip encapsulate explicit-null'],)
        )
