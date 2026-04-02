from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_neighbor_under_ospf


class TestConfigureNeighborUnderOspf(TestCase):

    def test_configure_neighbor_under_ospf(self):
        device = Mock()
        result = configure_neighbor_under_ospf(
            device,
            2,
            '55.55.55.2',
            10
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 2', 'neighbor 55.55.55.2 cost 10'],)
        )