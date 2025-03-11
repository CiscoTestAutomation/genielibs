from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import set_isis_timers
from unittest.mock import Mock


class TestSetIsisTimers(TestCase):

    def test_set_isis_timers(self):
        self.device = Mock()
        result = set_isis_timers(self.device, 6500, 5, 1, 50, 5, 1, 50, 5, 1, 50)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router isis', 'lsp-refresh-interval 6500', 'spf-interval 5 1 50', 'prc-interval 5 1 50', 'lsp-gen-interval 5 1 50'],)
        )
