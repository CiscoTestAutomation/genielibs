from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import configure_mpls_label_range
from unittest.mock import Mock


class TestConfigureMplsLabelRange(TestCase):

    def test_configure_mpls_label_range(self):
        self.device = Mock()
        result = configure_mpls_label_range(self.device, '16', '18', '20', '50')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('mpls label range 16 18 static 20 50',)
        )
