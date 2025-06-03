from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_redestribute_ospf_metric_in_bgp


class TestUnconfigureRedestributeOspfMetricInBgp(TestCase):

    def test_unconfigure_redestribute_ospf_metric_in_bgp(self):
        self.device = Mock()
        result = unconfigure_redestribute_ospf_metric_in_bgp(self.device, 1, 1, 100)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 1', 'no redistribute ospf 1 metric 100'],)
        )
