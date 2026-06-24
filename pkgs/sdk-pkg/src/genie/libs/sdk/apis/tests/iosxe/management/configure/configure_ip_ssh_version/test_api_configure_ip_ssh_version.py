import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_ip_ssh_version
)


class TestConfigureIpSshVersion(unittest.TestCase):

    def test_configure_ip_ssh_version(self):
        device = Mock()

        result = configure_ip_ssh_version(
            device,
            '2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip ssh version 2',)
        )

    def test_configure_ip_ssh_version_integer(self):
        device = Mock()

        result = configure_ip_ssh_version(
            device,
            2
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip ssh version 2',)
        )