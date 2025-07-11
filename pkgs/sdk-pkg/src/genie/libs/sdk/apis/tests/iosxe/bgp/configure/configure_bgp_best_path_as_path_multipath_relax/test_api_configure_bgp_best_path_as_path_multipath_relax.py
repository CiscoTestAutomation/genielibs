from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_best_path_as_path_multipath_relax
from unittest.mock import Mock

class TestConfigureBgpBestPathAsPathMultipathRelax(TestCase):

    def test_configure_bgp_best_path_as_path_multipath_relax(self):
        self.device = Mock()
        configure_bgp_best_path_as_path_multipath_relax(self.device, 100)
        self.device.configure.assert_called_with(['router bgp 100', 'bgp bestpath as-path multipath-relax'])
