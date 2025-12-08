from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import remove_tcp_keychain
from unittest.mock import Mock


class TestRemoveTcpKeychain(TestCase):

    def test_remove_tcp_keychain(self):
        self.device = Mock()
        result = remove_tcp_keychain(self.device, 'test1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no key chain test1'],)
        )
