from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_distribute_prefix_list_under_ospf


class TestConfigureDistributePrefixListUnderOspf(TestCase):

    def test_configure_distribute_prefix_list_under_ospf(self):
        device = Mock()
        result = configure_distribute_prefix_list_under_ospf(
            device,
            1,
            'ospf_prefix_list',
            'out',
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 1', 'distribute-list prefix ospf_prefix_list out'],)
        )