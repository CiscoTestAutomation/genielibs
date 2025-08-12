from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.configure import unconfigure_Usb
from unittest.mock import Mock


class TestUnconfigureUsb(TestCase):

    def test_unconfigure_Usb(self):
        self.device = Mock()
        result = unconfigure_Usb(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('platform usb disable',)
        )
