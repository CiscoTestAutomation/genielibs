import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_mdt_overlay_use_bgp,
)


class TestConfigureMdtOverlayUseBgp(unittest.TestCase):

    def test_configure_mdt_overlay_use_bgp(self):
        device = Mock()

        result = configure_mdt_overlay_use_bgp(
            device=device,
            vrf_name='vrf3001',
            address_family='ipv4',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'address-family ipv4',
                'mdt overlay use-bgp',
            ]
        )
