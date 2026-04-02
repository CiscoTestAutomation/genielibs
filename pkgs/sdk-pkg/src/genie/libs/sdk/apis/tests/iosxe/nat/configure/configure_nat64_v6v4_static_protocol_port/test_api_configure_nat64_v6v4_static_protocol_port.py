from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_v6v4_static_protocol_port

class TestConfigureNat64V6v4StaticProtocolPort(TestCase):

    def test_configure_nat64_v6v4_static_protocol_port(self):
        device = Mock()
        result = configure_nat64_v6v4_static_protocol_port(device, 'tcp', '2001:1::2', 1234, '1.1.1.2', 100)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['nat64 v6v4 static tcp 2001:1::2 1234 1.1.1.2 100'],)
        )