from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_pim_spt_threshold
from unittest.mock import Mock


class TestConfigurePimSptThreshold(TestCase):

    def test_configure_pim_spt_threshold(self):
        self.device = Mock()
        result = configure_pim_spt_threshold(self.device, 0)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip pim spt-threshold 0',)
        )
