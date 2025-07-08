from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.apphosting.configure import confirm_iox_enabled_requested_storage_media


class TestConfirmIoxEnabledRequestedStorageMedia(TestCase):

    def test_confirm_iox_enabled_requested_storage_media(self):
        device = Mock()
        device.parse = Mock(return_value={
            'internal_working_directory': '/vol/usb1'  
        })
        result = confirm_iox_enabled_requested_storage_media(device, storage='ssd')
        self.assertTrue(result)
        device.parse.assert_called_once_with('show app-hosting infra')