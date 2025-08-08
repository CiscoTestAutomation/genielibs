from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_redestribute_ospf_metric_in_bgp
from unittest.mock import Mock

class TestConfigureRedestributeOspfMetricInBgp(TestCase):

    def test_configure_redestribute_ospf_metric_in_bgp(self):
        self.device = Mock()
        configure_redestribute_ospf_metric_in_bgp(self.device, 1, 1, 100)
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 1', 'redistribute ospf 1 metric 100'],))