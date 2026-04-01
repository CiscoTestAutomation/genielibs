from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_ip_access_group_in_out

class TestUnconfigureIpAccessGroupInOut(TestCase):

    def test_unconfigure_ip_access_group_in_out(self):
        device = Mock()
        result = unconfigure_ip_access_group_in_out(device, 'Port-channel100', 'MSFT_PACL_IN', 'in')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Port-channel100', 'no ip access-group MSFT_PACL_IN in'],)
        )