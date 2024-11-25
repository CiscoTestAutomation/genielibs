import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import enable_radius_automate_tester_probe_on


class TestEnableRadiusAutomateTesterProbeOn(unittest.TestCase):

    def test_enable_radius_automate_tester_probe_on(self):
        self.device = Mock()
        enable_radius_automate_tester_probe_on(self.device, 'serv1', 'user1', 'red')
        self.device.configure.assert_called_once_with([
            "radius server serv1",
            "automate-tester username user1 probe-on vrf red"
        ])

    def test_enable_radius_automate_tester_probe_on_1(self):
        self.device = Mock()
        enable_radius_automate_tester_probe_on(self.device, 'serv1', 'user1')
        self.device.configure.assert_called_once_with([
            "radius server serv1",
            "automate-tester username user1 probe-on"
        ])
