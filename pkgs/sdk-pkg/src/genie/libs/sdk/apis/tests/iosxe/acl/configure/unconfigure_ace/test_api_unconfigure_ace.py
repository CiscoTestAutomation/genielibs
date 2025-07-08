from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_ace


class TestUnconfigureAce(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        unconfigure_ace(self.device, 'IN29', None, None, None, None, None, 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended IN29'] ,)
        )
