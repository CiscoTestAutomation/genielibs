from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_acl_with_src_dsc_net


class TestUnconfigureAclWithSrcDscNet(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        unconfigure_acl_with_src_dsc_net(self.device, '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no access-list 100'] ,)
        )
