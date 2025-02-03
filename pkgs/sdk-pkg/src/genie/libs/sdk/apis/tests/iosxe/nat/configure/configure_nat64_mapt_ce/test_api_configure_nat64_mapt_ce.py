from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat64_mapt_ce
from unittest.mock import Mock


class TestConfigureNat64MaptCe(TestCase):

    def test_configure_nat64_mapt_ce(self):
        self.device = Mock()
        result = configure_nat64_mapt_ce(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('nat64 settings map-t ce',)
        )
