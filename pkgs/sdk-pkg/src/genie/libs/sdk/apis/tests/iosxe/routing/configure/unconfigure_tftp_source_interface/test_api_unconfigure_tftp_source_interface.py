import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_tftp_source_interface
)


class TestUnconfigureTftpSourceInterface(unittest.TestCase):

    def test_unconfigure_tftp_source_interface(self):
        device = Mock()

        result = unconfigure_tftp_source_interface(
            device,
            'GigabitEthernet0/0'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip tftp source-interface GigabitEthernet0/0',)
        )