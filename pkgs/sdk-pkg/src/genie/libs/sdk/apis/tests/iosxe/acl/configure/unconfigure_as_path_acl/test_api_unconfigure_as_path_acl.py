from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_as_path_acl


class TestUnconfigureAsPathAcl(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        unconfigure_as_path_acl(self.device, '2', 'permit', '_300_')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip as-path access-list 2 permit _300_' ,)
        )
