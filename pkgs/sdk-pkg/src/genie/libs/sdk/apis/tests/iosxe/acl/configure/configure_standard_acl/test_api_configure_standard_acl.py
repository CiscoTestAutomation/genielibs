from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_standard_acl


class TestConfigureStandardAcl(TestCase):

    def test_configure_standard_acl(self):
        self.device = Mock()
        configure_standard_acl(self.device, 'Test5', '20', 'permit', 'host', '232.1.2.10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip access-list standard Test5\n20 permit host 232.1.2.10\n' ,)
        )
