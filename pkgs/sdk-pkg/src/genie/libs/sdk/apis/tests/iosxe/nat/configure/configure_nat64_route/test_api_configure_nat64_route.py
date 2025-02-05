from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_route
from unittest.mock import Mock


class TestConfigureNat64Route(TestCase):

    def test_configure_nat64_route(self):
        self.device = Mock()
        result = configure_nat64_route(self.device, '0.0.0.0/0', 'GigabitEthernet2', None, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('nat64 route  0.0.0.0/0 GigabitEthernet2',)
        )
