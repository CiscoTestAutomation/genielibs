from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_media_type
from unittest.mock import Mock


class TestUnconfigureInterfaceMediaType(TestCase):

    def test_unconfigure_interface_media_type(self):
        self.device = Mock()
        result = unconfigure_interface_media_type(self.device, 'GigabitEthernet0/0/0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/0', 'no media-type'],)
        )
