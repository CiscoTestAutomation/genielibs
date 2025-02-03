from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_mac_acl_etherType
from unittest.mock import Mock


class TestConfigureMacAclEthertype(TestCase):

    def test_configure_mac_acl_etherType(self):
        self.device = Mock()
        result = configure_mac_acl_etherType(self.device, 'profinetacl', 'permit', 34962, 0)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['mac access-list extended profinetacl', 'permit any any 34962 0'],)
        )
