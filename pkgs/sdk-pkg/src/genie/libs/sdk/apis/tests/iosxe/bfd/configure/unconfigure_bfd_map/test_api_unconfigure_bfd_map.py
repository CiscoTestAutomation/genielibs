from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import unconfigure_bfd_map
from unittest.mock import Mock


class TestUnconfigureBfdMap(TestCase):

    def test_unconfigure_bfd_map(self):
        self.device = Mock()
        result = unconfigure_bfd_map(self.device, 'bfd_temp', '10.10.10.1', '11.11.11.1', '32')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no bfd map ipv4 10.10.10.1/32 11.11.11.1/32 bfd_temp',)
        )
