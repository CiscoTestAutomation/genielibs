from unittest import TestCase
from genie.libs.sdk.apis.iosxe.spanning_tree.configure import \
    configure_spanning_tree_pathcost_method
from unittest.mock import Mock


class TestConfigureSpanningTreePathcostMethod(TestCase):

    def test_configure_spanning_tree_pathcost_method(self):
        self.device = Mock()
        result = configure_spanning_tree_pathcost_method(self.device, 'long')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['spanning-tree pathcost method long'],)
        )
