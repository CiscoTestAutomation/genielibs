from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9610.spanning_tree.configure import unconfigure_spanning_tree_portfast

class TestUnconfigureSpanningTreePortfast(TestCase):

    def test_unconfigure_spanning_tree_portfast(self):
        device = Mock()
        result = unconfigure_spanning_tree_portfast(device, True, True, False)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no spanning-tree portfast edge bpduguard default',)
        )

    def test_unconfigure_spanning_tree_portfast_1(self):
        device = Mock()
        result = unconfigure_spanning_tree_portfast(device, False, True, False)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no spanning-tree portfast edge bpduguard',)
        )

    def test_unconfigure_spanning_tree_portfast_2(self):
        device = Mock()
        result = unconfigure_spanning_tree_portfast(device, True, False, True)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no spanning-tree portfast edge bpdufilter default',)
        )