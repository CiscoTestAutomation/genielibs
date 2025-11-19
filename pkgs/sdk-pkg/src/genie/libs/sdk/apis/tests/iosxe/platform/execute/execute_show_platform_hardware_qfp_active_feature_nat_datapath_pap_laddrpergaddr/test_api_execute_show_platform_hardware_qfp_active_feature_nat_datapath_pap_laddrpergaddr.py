from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_hardware_qfp_active_feature_nat_datapath_pap_laddrpergaddr
from unittest.mock import Mock

class TestShowPlatformHardwareQfpActiveFeatureNatDatapathPapLaddrpergaddr(TestCase):

    def test_nat_datapath_pap_laddrpergaddr(self):
        self.device = Mock()
        execute_hardware_qfp_active_feature_nat_datapath_pap_laddrpergaddr(device=self.device)
        self.device.execute.assert_called_with('show platform hardware qfp active feature nat datapath pap laddrpergaddr')
