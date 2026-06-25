from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vpdn.configure import unconfigure_l2tp_class
from unittest.mock import Mock


class TestUnconfigureL2tpClass(TestCase):

    def test_unconfigure_l2tp_class(self):
        self.device = Mock()
        result = unconfigure_l2tp_class(self.device, 'L2TP_CLASS_011', True, 'cpe', 'cisco')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['l2tp-class L2TP_CLASS_011', 'no authentication', 'no hostname cpe', 'no password cisco'],)
        )
