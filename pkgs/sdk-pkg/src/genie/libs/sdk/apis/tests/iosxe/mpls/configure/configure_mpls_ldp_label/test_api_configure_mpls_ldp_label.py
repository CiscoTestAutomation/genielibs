from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import configure_mpls_ldp_label
from unittest.mock import Mock


class TestConfigureMplsLdpLabel(TestCase):

    def test_configure_mpls_ldp_label(self):
        self.device = Mock()
        result = configure_mpls_ldp_label(self.device, 'list1', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['mpls ldp label', 'allocate global prefix-list list1'],)
        )
