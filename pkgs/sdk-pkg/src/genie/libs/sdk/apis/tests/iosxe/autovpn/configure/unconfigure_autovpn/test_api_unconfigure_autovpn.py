from unittest import TestCase
from genie.libs.sdk.apis.iosxe.autovpn.configure import unconfigure_autovpn
from unittest.mock import Mock


class TestUnconfigureAutovpn(TestCase):

    def test_unconfigure_autovpn(self):
        self.device = Mock()
        result = unconfigure_autovpn(self.device, 'autovpn1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no crypto autovpn autovpn1',)
        )
