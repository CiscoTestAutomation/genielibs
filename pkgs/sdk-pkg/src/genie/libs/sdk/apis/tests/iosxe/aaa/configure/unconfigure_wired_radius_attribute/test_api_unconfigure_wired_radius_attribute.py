import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_wired_radius_attribute


class TestUnconfigureWiredRadiusAttribute(unittest.TestCase):

    def test_unconfigure_wired_radius_attribute(self):
        self.device = Mock()
        unconfigure_wired_radius_attribute(self.device, '6', 'support-multiple')
        self.device.configure.assert_called_with([
            'no radius-server attribute 6 support-multiple'
        ])
