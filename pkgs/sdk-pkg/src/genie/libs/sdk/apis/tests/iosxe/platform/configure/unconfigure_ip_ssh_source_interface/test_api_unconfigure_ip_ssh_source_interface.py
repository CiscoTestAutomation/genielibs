import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_ip_ssh_source_interface


class TestUnconfigureIpSshSourceInterface(unittest.TestCase):

    def test_unconfigure_ip_ssh_source_interface(self):
        device = Mock()

        result = unconfigure_ip_ssh_source_interface(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip ssh source-interface',)
        )