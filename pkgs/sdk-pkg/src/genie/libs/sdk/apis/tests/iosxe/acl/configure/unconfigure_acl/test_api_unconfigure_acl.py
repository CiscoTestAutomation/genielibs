from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_acl


class TestUnconfigureAcl(TestCase):

    def test_unconfigure_acl(self):
        self.device = Mock()
        unconfigure_acl(self.device, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip access-list extended True' ,)
        )
