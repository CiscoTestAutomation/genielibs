from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_as_path_acl


class TestConfigureAsPathAcl(TestCase):

    def test_configure_as_path_acl(self):
        self.device = Mock()
        configure_as_path_acl(self.device, '2', 'permit', '_300_')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip as-path access-list 2 permit _300_',)
        )
