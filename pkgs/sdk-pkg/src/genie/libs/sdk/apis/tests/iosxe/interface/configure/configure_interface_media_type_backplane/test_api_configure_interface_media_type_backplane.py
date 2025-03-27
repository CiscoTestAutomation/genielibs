from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_media_type_backplane
from unittest.mock import Mock


class TestConfigureInterfaceMediaTypeBackplane(TestCase):

    def test_configure_interface_media_type_backplane(self):
        self.device = Mock()
        result = configure_interface_media_type_backplane(self.device, 'TenGigabitEthernet1/2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet1/2', 'media-type backplane'],)
        )
