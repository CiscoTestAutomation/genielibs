from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_update_source
from unittest.mock import Mock


class TestConfigureBgpUpdateSource(TestCase):

    def test_configure_bgp_update_source(self):
        self.device = Mock()
        result = configure_bgp_update_source(self.device, 200, '102.0.1.2', 'Loopback15')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 200', 'neighbor 102.0.1.2 update-source Loopback15'],)
        )
