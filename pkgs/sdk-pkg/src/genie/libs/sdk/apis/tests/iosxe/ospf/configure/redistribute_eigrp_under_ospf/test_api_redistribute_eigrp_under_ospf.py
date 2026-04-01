from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import redistribute_eigrp_under_ospf


class TestRedistributeEigrpUnderOspf(TestCase):

    def test_redistribute_eigrp_under_ospf(self):
        device = Mock()
        result = redistribute_eigrp_under_ospf(
            device,
            1,
            1,
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 1', 'redistribute eigrp 1'],)
        )