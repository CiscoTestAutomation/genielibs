from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hsr.configure import unconfigure_hsr_hsr_mode
from unittest.mock import Mock


class TestUnconfigureHsrHsrMode(TestCase):

    def test_unconfigure_hsr_hsr_mode(self):
        self.device = Mock()
        result = unconfigure_hsr_hsr_mode(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no hsr-hsr-mode enable',)
        )
