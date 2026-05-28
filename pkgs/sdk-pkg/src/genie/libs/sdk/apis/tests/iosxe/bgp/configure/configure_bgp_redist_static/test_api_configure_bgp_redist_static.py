from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_redist_static
from unittest.mock import Mock


class TestConfigureBgpRedistStatic(TestCase):

    def test_configure_bgp_redist_static(self):
        self.device = Mock()
        result = configure_bgp_redist_static(self.device, 200)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 200', 'redistribute static'],)
        )
