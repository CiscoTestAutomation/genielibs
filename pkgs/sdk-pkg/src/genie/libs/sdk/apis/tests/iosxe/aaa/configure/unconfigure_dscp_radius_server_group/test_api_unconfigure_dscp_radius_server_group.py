import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_dscp_radius_server_group


class TestUnconfigureDscpRadiusServerGroup(unittest.TestCase):

    def test_unconfigure_dscp_radius_server_group(self):
        self.device = Mock()
        unconfigure_dscp_radius_server_group(self.device, 'ISEGRP2', None, None)
        self.device.configure.assert_called_with([
            'aaa group server radius ISEGRP2'
        ])

    def test_unconfigure_dscp_radius_server_group_1(self):
        self.device = Mock()
        unconfigure_dscp_radius_server_group(self.device, 'ISEGRP2', '40', '32')
        self.device.configure.assert_called_with([
            'aaa group server radius ISEGRP2',
            'no dscp auth 40',
            'no dscp acct 32'
        ])
