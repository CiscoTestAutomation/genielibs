from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import  unconfigure_interface_range_dhcp_channel_group_mode


class  TestUnconfigureInterfaceRangeDhcpChannelGroupMode(TestCase):

    def test_unconfigure_interface_range_dhcp_channel_group_mode(self):
        self.device = Mock()
        unconfigure_interface_range_dhcp_channel_group_mode(self.device, 'Gi1/0/39', '41', '200', 'desirable')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface range Gi1/0/39 - 41",
                    "no channel-group 200 mode desirable"],))