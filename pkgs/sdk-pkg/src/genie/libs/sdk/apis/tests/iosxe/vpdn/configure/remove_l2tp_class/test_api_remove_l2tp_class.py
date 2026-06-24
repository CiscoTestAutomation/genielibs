from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vpdn.configure import remove_l2tp_class
from unittest.mock import Mock


class TestRemoveL2tpClass(TestCase):

    def test_remove_l2tp_class(self):
        self.device = Mock()
        result = remove_l2tp_class(self.device, 'L2TP_CLASS_011')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no l2tp-class L2TP_CLASS_011',)
        )
