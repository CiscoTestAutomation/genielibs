from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import unconfigure_rep_ztp
from unittest.mock import Mock


class TestUnconfigureRepZtp(TestCase):

    def test_unconfigure_rep_ztp(self):
        self.device = Mock()
        result = unconfigure_rep_ztp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no rep ztp',)
        )
