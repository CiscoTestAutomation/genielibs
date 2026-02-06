from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_ip_tcp_adjust_mss
from unittest.mock import Mock


class TestConfigureInterfaceIpTcpAdjustMss(TestCase):

    def test_configure_interface_ip_tcp_adjust_mss(self):
        self.device = Mock()
        result = configure_interface_ip_tcp_adjust_mss(self.device, 'Te1/0/7', '1400', 'False')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Te1/0/7', 'no switchport', 'ip tcp adjust-mss 1400'],)
        )
