from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import disable_bfd_static_route
from unittest.mock import Mock


class TestDisableBfdStaticRoute(TestCase):

    def test_disable_bfd_static_route(self):
        self.device = Mock()
        result = disable_bfd_static_route(self.device, 'TenGigabitEthernet1/0/14', '10.1.1.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip route static bfd TenGigabitEthernet1/0/14 10.1.1.1'],)
        )
