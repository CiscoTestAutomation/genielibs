from unittest import TestCase
from unittest.mock import Mock, patch
from genie.libs.sdk.apis.iosxe.apphosting.configure import enable_usb_ssd_verify_exists


class TestEnableUsbSsdVerifyExists(TestCase):

    @patch('time.sleep', return_value=None)  # Patch time.sleep to avoid delay
    def test_enable_usb_ssd_verify_exists(self, mock_sleep):
        self.device = Mock()
        self.device.api.get_show_output_include = Mock(return_value=[True])
        self.device.api.enable_usb_ssd = Mock()
        self.device.parse = Mock(return_value={
            'version': {
                'disks': {
                    'usbflash1:.': 'Some storage info'
                }
            }
        })

        enable_usb_ssd_verify_exists(self.device, 'usbflash1:.', 30)
        self.device.api.get_show_output_include.assert_called_once_with(
            command='show running-config',
            filter='platform usb disable'
        )

        self.device.api.enable_usb_ssd.assert_called_once()
        self.device.parse.assert_called_once_with("show version")
        mock_sleep.assert_called_once_with(30)