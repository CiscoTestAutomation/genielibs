from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_mpls_ldp_advertise


class TestUnconfigureMplsLdpAdvertise(TestCase):

    def test_unconfigure_mpls_ldp_advertise(self):
        device = Mock()

        result = unconfigure_mpls_ldp_advertise(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no mpls ldp advertise-labels")
