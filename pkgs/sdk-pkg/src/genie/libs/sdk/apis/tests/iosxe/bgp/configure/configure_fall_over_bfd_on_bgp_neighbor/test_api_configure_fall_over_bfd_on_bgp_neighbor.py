from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_fall_over_bfd_on_bgp_neighbor

class TestConfigureFallOverBfdOnBgpNeighbor(TestCase):

    def test_configure_fall_over_bfd_on_bgp_neighbor(self):
        device = Mock()
        result = configure_fall_over_bfd_on_bgp_neighbor(device, 1, 'pg-ibgp-rc')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router bgp 1', 'neighbor pg-ibgp-rc fall-over bfd'],)
        )