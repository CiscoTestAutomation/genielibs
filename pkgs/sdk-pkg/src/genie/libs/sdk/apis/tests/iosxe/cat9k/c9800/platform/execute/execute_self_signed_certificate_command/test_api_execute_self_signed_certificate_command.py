import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.execute import execute_self_signed_certificate_command


class TestExecuteSelfSignedCertificateCommand(unittest.TestCase):

    def test_execute_self_signed_certificate_command(self):
        device = Mock()

        result = execute_self_signed_certificate_command(
            device, 'Cisco@123', 2048, 'sha256', 0, 300
        )

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'wireless config vwlc-ssc key-size 2048 signature-algo sha256 '
            'password 0 Cisco@123'
        )
