from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_mac_acl
from unittest.mock import Mock


class TestUnconfigureMacAcl(TestCase):

    def test_unconfigure_mac_acl(self):
        self.device = Mock()
        result = unconfigure_mac_acl(self.device, 'acl1', 'permit', 'any', '1111.1111.1111', 'etype-6000')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['mac access-list extended acl1', 'no permit any host 1111.1111.1111 etype-6000'],)
        )
