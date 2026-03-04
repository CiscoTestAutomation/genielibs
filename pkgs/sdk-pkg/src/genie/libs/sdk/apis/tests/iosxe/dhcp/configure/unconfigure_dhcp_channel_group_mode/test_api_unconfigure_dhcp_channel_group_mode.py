import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_channel_group_mode


class TestUnconfigureDhcpChannelGroupMode(TestCase):

    def test_unconfigure_dhcp_channel_group_mode(self):
        device = Mock()
        result = unconfigure_dhcp_channel_group_mode(device, 'Gig1/0/1', '10', 'active')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with([
            'interface Gig1/0/1',
            'no channel-group 10 mode active'
        ])


if __name__ == '__main__':
    unittest.main()