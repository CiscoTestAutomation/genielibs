import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_range_dhcp_channel_group_mode


class TestConfigureInterfaceRangeDhcpChannelGroupMode(TestCase):

    def test_configure_interface_range_dhcp_channel_group_mode(self):
        device = Mock()
        result = configure_interface_range_dhcp_channel_group_mode(device, 'Gi1/0/39', '41', '200', 'desirable')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface range Gi1/0/39 - 41', 'channel-group 200 mode desirable'],)
        )


if __name__ == '__main__':
    unittest.main()