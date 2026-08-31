from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_pim_spt_threshold
from unittest.mock import Mock


class TestUnconfigurePimSptThreshold(TestCase):

    def test_unconfigure_pim_spt_threshold(self):
        self.device = Mock()
        result = unconfigure_pim_spt_threshold(self.device, 0)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip pim spt-threshold 0',)
        )
