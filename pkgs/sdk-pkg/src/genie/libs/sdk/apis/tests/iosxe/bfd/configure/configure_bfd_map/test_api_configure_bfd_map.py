from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import configure_bfd_map
from unittest.mock import Mock


class TestConfigureBfdMap(TestCase):

    def test_configure_bfd_map(self):
        self.device = Mock()
        result = configure_bfd_map(self.device, 'bfd_temp', '10.10.10.1', '11.11.11.1', '32')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('bfd map ipv4 10.10.10.1/32 11.11.11.1/32 bfd_temp',)
        )
