from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import delete_configure_ipv6_acl


class TestDeleteConfigureIpv6Acl(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        delete_configure_ipv6_acl(self.device, 'racl1', 'permit', '2001::2', '3001::2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 access-list racl1', 'no permit ipv6 host 2001::2 host 3001::2'] ,)
        )
