from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_mac_acl


class TestConfigureMacAcl(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        configure_mac_acl(self.device, 'test', 'permit', '1111.2222.3333', '2444.2333.2222', 'etype-6000')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['mac access-list extended test', 'permit host 1111.2222.3333 host 2444.2333.2222 etype-6000'] ,)
        )
