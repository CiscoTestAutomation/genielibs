from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_label_mode_all_explicit_null
from unittest.mock import Mock

class TestConfigureLabelModeAllExplicitNull(TestCase):

    def test_configure_label_mode_all_explicit_null(self):
        self.device = Mock()
        configure_label_mode_all_explicit_null(self.device, '200', 'ipv6')
        self.assertEqual(self.device.configure.mock_calls[0].args,('router bgp 200\naddress-family ipv6\nlabel mode all-explicit-null\n',))