from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.configure import configure_Usb
from unittest.mock import Mock


class TestConfigureUsb(TestCase):

    def test_configure_Usb(self):
        self.device = Mock()
        result = configure_Usb(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no platform usb disable',)
        )
