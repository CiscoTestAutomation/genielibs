from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_mac_acl
from unittest.mock import Mock


class TestConfigureMacAcl(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        result = configure_mac_acl(self.device, 'acl1', 'permit', 'any', '1111.1111.1111', 'etype-6000')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['mac access-list extended acl1', 'permit any host 1111.1111.1111 etype-6000'],)
        )
