from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_extended_acl_with_dscp
from unittest.mock import Mock


class TestConfigureExtendedAclWithDscp(TestCase):

    def test_configure_extended_acl_with_dscp(self):
        self.device = Mock()
        result = configure_extended_acl_with_dscp(self.device, '100', 10, 'permit', '131.1.1.2', '162.1.1.2', 7)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended 100', '10 permit ip host 131.1.1.2 host 162.1.1.2 dscp 7'],)
        )
