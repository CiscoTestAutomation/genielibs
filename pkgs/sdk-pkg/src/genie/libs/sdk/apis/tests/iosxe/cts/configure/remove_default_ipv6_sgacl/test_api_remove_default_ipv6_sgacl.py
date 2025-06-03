from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import remove_default_ipv6_sgacl
from unittest.mock import Mock


class TestRemoveDefaultIpv6Sgacl(TestCase):

    def test_remove_default_ipv6_sgacl(self):
        self.device = Mock()
        result = remove_default_ipv6_sgacl(self.device, 'DEFAULT_PERMIT_v6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts role-based permissions default ipv6 DEFAULT_PERMIT_v6'],)
        )
