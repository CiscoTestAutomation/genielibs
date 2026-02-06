from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_mpls_ldp_label
from unittest.mock import Mock


class TestUnconfigureMplsLdpLabel(TestCase):

    def test_unconfigure_mpls_ldp_label(self):
        self.device = Mock()
        result = unconfigure_mpls_ldp_label(self.device, 'list1', False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['mpls ldp label', 'no allocate global prefix-list list1'],)
        )
