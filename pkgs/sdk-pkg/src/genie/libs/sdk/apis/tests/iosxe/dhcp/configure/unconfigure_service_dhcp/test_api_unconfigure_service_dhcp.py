from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_service_dhcp
from unittest.mock import Mock


class TestUnconfigureServiceDhcp(TestCase):

    def test_unconfigure_service_dhcp(self):
        self.device = Mock()
        unconfigure_service_dhcp(self.device)
        self.assertEqual(self.device.configure.mock_calls[0].args,('no service dhcp',))
