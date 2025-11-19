from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_mpls_ldp_neighbor_labels_accept
from unittest.mock import Mock


class TestUnconfigureMplsLdpNeighborLabelsAccept(TestCase):

    def test_unconfigure_mpls_ldp_neighbor_labels_accept(self):
        self.device = Mock()
        result = unconfigure_mpls_ldp_neighbor_labels_accept(self.device, '10.12.12.12', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no mpls ldp neighbor 10.12.12.12 labels accept 1',)
        )
