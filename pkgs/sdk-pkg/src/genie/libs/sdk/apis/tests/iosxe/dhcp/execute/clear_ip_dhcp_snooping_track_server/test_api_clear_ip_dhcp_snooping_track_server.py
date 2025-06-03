from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.execute import clear_ip_dhcp_snooping_track_server
from unittest.mock import Mock

class TestClearIpDhcpSnoopingTrackServer(TestCase):

    def test_clear_ip_dhcp_snooping_track_server(self):
        self.device = Mock()
        clear_ip_dhcp_snooping_track_server(self.device)
        self.device.execute.assert_called_with('clear ip dhcp snooping track server all')
