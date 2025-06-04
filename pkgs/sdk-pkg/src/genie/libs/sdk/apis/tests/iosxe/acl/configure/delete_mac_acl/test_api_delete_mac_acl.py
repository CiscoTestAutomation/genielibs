from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import delete_mac_acl


class TestDeleteMacAcl(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        delete_mac_acl(self.device, 'test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no mac access-list extended test'] ,)
        )
