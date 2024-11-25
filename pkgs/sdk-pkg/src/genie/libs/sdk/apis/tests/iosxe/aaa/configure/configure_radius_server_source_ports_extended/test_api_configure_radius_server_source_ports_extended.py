import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_server_source_ports_extended


class TestConfigureRadiusServerSourcePortsExtended(unittest.TestCase):

    def test_configure_radius_server_source_ports_extended(self):
        self.device = Mock()
        configure_radius_server_source_ports_extended(self.device)
        self.device.configure.assert_called_once_with([
            'radius-server source-ports extended'
        ])