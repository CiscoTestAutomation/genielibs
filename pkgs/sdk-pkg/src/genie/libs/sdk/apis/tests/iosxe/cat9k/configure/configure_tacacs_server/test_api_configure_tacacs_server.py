from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.configure import configure_tacacs_server

class TestConfigureTacacsServer(TestCase):

    def test_configure_tacacs_server(self):
        device = Mock()
        result = configure_tacacs_server(
            device,
            {'host': 'abc', 'key': 'cisco', 'server': '10.1.2.3'}
        )
        expected_output = ['tacacs server abc', 'address ipv4 10.1.2.3', 'key cisco']
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (expected_output,)
        )