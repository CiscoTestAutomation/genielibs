from unittest import TestCase
from genie.libs.sdk.apis.iosxe.spanning_tree.get import get_configure_spanning_tree_guard_root_output
from unittest.mock import Mock


class TestGetConfigureSpanningTreeGuardRootOutput(TestCase):

    def test_get_configure_spanning_tree_guard_root_output(self):
        self.device = Mock()
        result = get_configure_spanning_tree_guard_root_output(self.device, 'GigabitEthernet0/1/0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/1/0', 'spanning-tree guard root'],)
        )
