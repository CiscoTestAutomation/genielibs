from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.arp.configure import unconfigure_static_arp


class TestUnconfigureStaticArp(TestCase):

    def test_unconfigure_static_arp(self):
        device = Mock()
        unconfigure_static_arp(device, "10.1.1.1", "aabb.ccdd.eeff")
        device.configure.assert_called_once_with(
            "no arp 10.1.1.1 aabb.ccdd.eeff ARPA"
        )

    def test_unconfigure_static_arp_failure(self):
        device = Mock()
        device.name = "R1"
        device.configure.side_effect = SubCommandFailure("cli error")
        with self.assertRaises(SubCommandFailure):
            unconfigure_static_arp(device, "10.1.1.1", "aabb.ccdd.eeff")
