from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_acl_with_src_dsc_net


class TestConfigureAclWithSrcDscNet(TestCase):

    def test_configure_acl_with_src_dsc_net(self):
        self.device = Mock()
        configure_acl_with_src_dsc_net(self.device, '100', 'permit', '10.0.35.0', '0.0.0.255', '10.0.36.0', '0.0.0.255')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['access-list 100 permit ip 10.0.35.0 0.0.0.255 10.0.36.0 0.0.0.255'],)
        )
