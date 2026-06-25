from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vpdn.configure import configure_l2tp_class
from unittest.mock import Mock


class TestConfigureL2tpClass(TestCase):

    def test_configure_l2tp_class(self):
        self.device = Mock()
        result = configure_l2tp_class(self.device, 'L2TP_CLASS_011', True, 'cpe', 'cisco')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['l2tp-class L2TP_CLASS_011', 'authentication', 'hostname cpe', 'password cisco'],)
        )
