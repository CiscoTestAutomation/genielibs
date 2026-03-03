from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9500.spanning_tree.configure import configure_spanning_tree_portfast

class TestConfigureSpanningTreePortfast(TestCase):

    def test_configure_spanning_tree_portfast(self):
        device = Mock()
        result = configure_spanning_tree_portfast(device, True, True, False, 'edge')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('spanning-tree portfast edge bpduguard default',)
        )

    def test_configure_spanning_tree_portfast_1(self):
        device = Mock()
        result = configure_spanning_tree_portfast(device, False, True, False, 'edge')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('spanning-tree portfast edge bpduguard',)
        )

    def test_configure_spanning_tree_portfast_2(self):
        device = Mock()
        result = configure_spanning_tree_portfast(device, True, False, True, 'edge')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('spanning-tree portfast edge bpdufilter default',)
        )