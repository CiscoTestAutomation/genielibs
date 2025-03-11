from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_pool
from unittest.mock import Mock


class TestConfigureDhcpPool(TestCase):

    def test_configure_dhcp_pool(self):
        self.device = Mock()
        result = configure_dhcp_pool(self.device, 'POOL_88', None, None, None, None, None, 'True', None, None, None, 'infinite')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip dhcp pool POOL_88', 'lease infinite'],)
        )
