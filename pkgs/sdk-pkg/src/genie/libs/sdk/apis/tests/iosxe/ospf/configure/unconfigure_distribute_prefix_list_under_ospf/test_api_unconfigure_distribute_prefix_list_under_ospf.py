from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import unconfigure_distribute_prefix_list_under_ospf


class TestUnconfigureDistributePrefixListUnderOspf(TestCase):

    def test_unconfigure_distribute_prefix_list_under_ospf(self):
        device = Mock()
        result = unconfigure_distribute_prefix_list_under_ospf(
            device,
            1,
            'ospf_prefix_list',
            'out',
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 1', 'no distribute-list prefix ospf_prefix_list out'],)
        )