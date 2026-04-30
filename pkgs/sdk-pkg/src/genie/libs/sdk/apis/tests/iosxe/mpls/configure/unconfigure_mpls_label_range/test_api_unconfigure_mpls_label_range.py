from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_mpls_label_range
from unittest.mock import Mock


class TestUnconfigureMplsLabelRange(TestCase):

    def test_unconfigure_mpls_label_range(self):
        self.device = Mock()
        result = unconfigure_mpls_label_range(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no mpls label range',)
        )
