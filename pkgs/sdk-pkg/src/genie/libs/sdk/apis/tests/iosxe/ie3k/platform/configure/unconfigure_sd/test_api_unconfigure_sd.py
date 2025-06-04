from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.configure import unconfigure_sd
from unittest.mock import Mock


class TestUnconfigureSd(TestCase):

    def test_unconfigure_sd(self):
        self.device = Mock()
        result = unconfigure_sd(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('platform sd disable',)
        )
