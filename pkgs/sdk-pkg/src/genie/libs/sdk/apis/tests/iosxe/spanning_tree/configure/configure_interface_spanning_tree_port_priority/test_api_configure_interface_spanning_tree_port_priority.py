from unittest import TestCase
from genie.libs.sdk.apis.iosxe.spanning_tree.configure import \
    configure_interface_spanning_tree_port_priority
from unittest.mock import Mock


class TestConfigureInterfaceSpanningTreePortPriority(TestCase):

    def test_configure_interface_spanning_tree_port_priority(self):
        self.device = Mock()
        result = configure_interface_spanning_tree_port_priority(
            self.device, 'GigabitEthernet0/1/1', '64'
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/1/1',
              'spanning-tree port-priority 64'],)
        )
