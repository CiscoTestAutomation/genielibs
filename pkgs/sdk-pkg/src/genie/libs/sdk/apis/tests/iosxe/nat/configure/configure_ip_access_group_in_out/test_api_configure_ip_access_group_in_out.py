from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_ip_access_group_in_out

class TestConfigureIpAccessGroupInOut(TestCase):

    def test_configure_ip_access_group_in_out(self):
        device = Mock()
        result = configure_ip_access_group_in_out(device, 'Port-channel100', 'MSFT_PACL_IN', 'in')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Port-channel100', 'ip access-group MSFT_PACL_IN in'],)
        )