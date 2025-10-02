from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nbar.configure import unconfig_trust_points
from unittest.mock import Mock


class TestUnconfigTrustPoints(TestCase):

    def test_unconfig_trust_points(self):
        self.device = Mock()
        results_map = {
            'clear ip nbar protocol-discovery': 'Clear all NBAR Protocol Discovery statistics? [yes]: yes Cleared NBAR Protocol Discovery statistics on all interfaces.',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = unconfig_trust_points(self.device)
        self.assertIn(
            'clear ip nbar protocol-discovery',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
