from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mpls.configure import configure_mpls_ldp_advertise


class TestConfigureMplsLdpAdvertise(TestCase):

    def test_configure_mpls_ldp_advertise(self):
        device = Mock()

        result = configure_mpls_ldp_advertise(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("mpls ldp advertise-labels")
