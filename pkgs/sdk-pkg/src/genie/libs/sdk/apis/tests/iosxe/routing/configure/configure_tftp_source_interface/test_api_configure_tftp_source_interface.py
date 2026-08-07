import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    configure_tftp_source_interface
)


class TestConfigureTftpSourceInterface(unittest.TestCase):

    def test_configure_tftp_source_interface(self):
        device = Mock()

        result = configure_tftp_source_interface(
            device,
            'GigabitEthernet0/0'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip tftp source-interface GigabitEthernet0/0',)
        )