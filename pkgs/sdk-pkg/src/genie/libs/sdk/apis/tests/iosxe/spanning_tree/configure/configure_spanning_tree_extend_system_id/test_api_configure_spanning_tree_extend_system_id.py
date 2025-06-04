from unittest import TestCase
from genie.libs.sdk.apis.iosxe.spanning_tree.configure import configure_spanning_tree_extend_system_id
from unittest.mock import Mock


class TestConfigureSpanningTreeExtendSystemId(TestCase):

    def test_configure_spanning_tree_extend_system_id(self):
        self.device = Mock()
        result = configure_spanning_tree_extend_system_id(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('spanning-tree extend system-id',)
        )
