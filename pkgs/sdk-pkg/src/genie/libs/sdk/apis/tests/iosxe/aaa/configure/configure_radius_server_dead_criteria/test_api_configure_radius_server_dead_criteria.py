import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_server_dead_criteria


class TestConfigureRadiusServerDeadCriteria(unittest.TestCase):

    def test_configure_radius_server_dead_criteria(self):
        self.device = Mock()
        configure_radius_server_dead_criteria(self.device, '2', '1')
        self.device.configure.assert_called_once_with([
            "radius-server dead-criteria time 2 tries 1"
        ])
        
