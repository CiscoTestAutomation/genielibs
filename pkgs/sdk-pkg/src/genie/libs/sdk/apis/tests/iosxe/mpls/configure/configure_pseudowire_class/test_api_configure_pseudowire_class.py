from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import configure_pseudowire_class
from unittest.mock import Mock


class TestConfigurePseudowireClass(TestCase):

    def test_configure_pseudowire_class(self):
        self.device = Mock()
        result = configure_pseudowire_class(self.device, 'PW_CLASS_011', 'l2tpv2', 'l2tpv2 L2TP_CLASS_011', 'Dialer10', True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['pseudowire-class PW_CLASS_011', 'encapsulation l2tpv2', 'protocol l2tpv2 L2TP_CLASS_011', 'ip local interface Dialer10', 'ip tos reflect'],)
        )
