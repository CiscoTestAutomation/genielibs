import unittest

from genie.libs.sdk.apis.iosxr.pki.configure import (
    configure_trustpoint,
    unconfigure_trustpoint,
    configure_pki_authenticate_certificate,
)

from ats.topology import Device
from unittest import mock

class TestConfigureTrustpoint(unittest.TestCase):
    def setUp(self):
        self.device = mock.MagicMock(spec=Device)
        self.device.configure = mock.MagicMock()
        self.device.execute = mock.MagicMock()

    def test_configure_trustpoint(self):
        self.device.configure = mock.MagicMock()
        configure_trustpoint(self.device, 'TEST_TP')
        self.device.configure.assert_called_with([
            'crypto ca trustpoint TEST_TP',
            'enrollment terminal'
        ])

    def test_unconfigure_trustpoint(self):
        self.device.configure = mock.MagicMock()
        unconfigure_trustpoint(self.device, 'TEST_TP')
        self.device.configure.assert_called_with('no crypto ca trustpoint TEST_TP')

    def test_configure_pki_authenticate_certificate(self    ):
        self.device.configure = mock.MagicMock()
        certificate = """Dummy Certificate"""
        configure_pki_authenticate_certificate(self.device, certificate, 'TEST_TP')
        self.device.execute.assert_called()