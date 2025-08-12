from unittest import TestCase
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_static_arp
from unittest.mock import Mock


class TestUnconfigureStaticArp(TestCase):

    def test_unconfigure_static_arp(self):
        self.device = Mock()
        result = unconfigure_static_arp(self.device, '10.189.216.204', '1234.5678.9abc')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no arp 10.189.216.204 1234.5678.9abc arpa',)
        )
