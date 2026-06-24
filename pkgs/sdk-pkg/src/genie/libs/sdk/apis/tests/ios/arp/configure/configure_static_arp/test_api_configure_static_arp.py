from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.arp.configure import configure_static_arp


class TestConfigureStaticArp(TestCase):

    def test_configure_static_arp(self):
        device = Mock()
        configure_static_arp(device, "10.1.1.1", "aabb.ccdd.eeff")
        device.configure.assert_called_once_with(
            "arp 10.1.1.1 aabb.ccdd.eeff ARPA"
        )

    def test_configure_static_arp_failure(self):
        device = Mock()
        device.name = "R1"
        device.configure.side_effect = SubCommandFailure("cli error")
        with self.assertRaises(SubCommandFailure):
            configure_static_arp(device, "10.1.1.1", "aabb.ccdd.eeff")
