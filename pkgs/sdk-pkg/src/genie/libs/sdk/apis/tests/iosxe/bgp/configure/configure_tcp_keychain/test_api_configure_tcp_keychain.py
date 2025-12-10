from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_tcp_keychain
from unittest.mock import Mock


class TestConfigureTcpKeychain(TestCase):

    def test_configure_tcp_keychain(self):
        self.device = Mock()
        result = configure_tcp_keychain(self.device, 'test1', {'accept-ao-mismatch': True,
 'accept_lifetime': 'local 00:00:00 Jan 1 2025 infinite',
 'algorithm': 'hmac-sha-1',
 'id': 1,
 'recv_id': '2',
 'send_id': '2',
 'send_lifetime': 'local 00:00:00 Jan 1 2025 infinite',
 'string': 'cisco123',
 'type': 'tcp'})
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['key chain test1 tcp', 'key 1', 'send-id 2', 'recv-id 2', 'key-string cisco123', 'accept-lifetime local 00:00:00 Jan 1 2025 infinite', 'send-lifetime local 00:00:00 Jan 1 2025 infinite', 'cryptographic-algorithm hmac-sha-1', 'accept-ao-mismatch'],)
        )
