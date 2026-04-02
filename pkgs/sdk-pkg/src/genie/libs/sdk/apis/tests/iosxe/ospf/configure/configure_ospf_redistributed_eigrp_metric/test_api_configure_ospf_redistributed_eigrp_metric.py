from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_redistributed_eigrp_metric


class TestConfigureOspfRedistributedEigrpMetric(TestCase):

    def test_configure_ospf_redistributed_eigrp_metric(self):
        device = Mock()
        result = configure_ospf_redistributed_eigrp_metric(
            device,
            '101',
            '101',
            '1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 101', 'redistribute eigrp 101 metric-type 1 subnets'],)
        )