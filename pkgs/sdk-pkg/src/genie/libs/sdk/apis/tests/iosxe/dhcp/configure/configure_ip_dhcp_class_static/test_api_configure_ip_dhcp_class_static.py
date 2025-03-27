from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_class_static
from unittest.mock import Mock


class TestConfigureIpDhcpClassStatic(TestCase):

    def test_configure_ip_dhcp_class_static(self):
        self.device = Mock()
        result = configure_ip_dhcp_class_static(self.device, 'static', None, 'True', 'aabbcc', 'ffffff')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip dhcp class static', 'relay agent information', 'relay-information hex aabbcc mask ffffff'],)
        )
