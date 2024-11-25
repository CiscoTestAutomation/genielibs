import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_radius_server_dead_criteria


class TestUnconfigureRadiusServerDeadCriteria(unittest.TestCase):

    def test_unconfigure_radius_server_dead_criteria(self):
        self.device = Mock()
        unconfigure_radius_server_dead_criteria(self.device, '2', '1')
        self.device.configure.assert_called_with([
            'no radius-server dead-criteria time 2 tries 1'
        ])
