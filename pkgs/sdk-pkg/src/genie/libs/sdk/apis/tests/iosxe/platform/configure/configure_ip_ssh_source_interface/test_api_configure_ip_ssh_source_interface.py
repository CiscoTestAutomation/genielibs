import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_ssh_source_interface


class TestConfigureIpSshSourceInterface(unittest.TestCase):

    def test_configure_ip_ssh_source_interface(self):
        device = Mock()

        result = configure_ip_ssh_source_interface(device, 'Gig0')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip ssh source-interface Gig0',)
        )