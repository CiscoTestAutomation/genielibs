import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_dscp_radius_server


class TestUnconfigureDscpRadiusServer(unittest.TestCase):

    def test_unconfigure_dscp_radius_server(self):
        self.device = Mock()
        unconfigure_dscp_radius_server(self.device, 'ISE2.7', None, None)
        self.device.configure.assert_called_with([
            'radius server ISE2.7'
        ])

    def test_unconfigure_dscp_radius_server_1(self):
        self.device = Mock()
        unconfigure_dscp_radius_server(self.device, 'ISE2.7', '20', '10')
        self.device.configure.assert_called_with([
            'radius server ISE2.7',
            'no dscp auth 20',
            'no dscp acct 10'
        ])
