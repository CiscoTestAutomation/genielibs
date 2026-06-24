from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_pseudowire_class
from unittest.mock import Mock


class TestUnconfigurePseudowireClass(TestCase):

    def test_unconfigure_pseudowire_class(self):
        self.device = Mock()
        result = unconfigure_pseudowire_class(self.device, 'PW_CLASS_011', 'l2tpv2', 'l2tpv2 L2TP_CLASS_011', 'Dialer10', True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['pseudowire-class PW_CLASS_011', 'no encapsulation l2tpv2', 'no protocol l2tpv2 L2TP_CLASS_011', 'no ip local interface Dialer10', 'no ip tos reflect'],)
        )
