import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_channel_group_mode


class TestConfigureDhcpChannelGroupMode(TestCase):

    def test_configure_dhcp_channel_group_mode(self):
        device = Mock()
        result = configure_dhcp_channel_group_mode(device, 'Gig1/0/1', '10', 'active')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Gig1/0/1', 'channel-group 10 mode active'],)
        )


if __name__ == '__main__':
    unittest.main()