import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    unconfigure_mdt_overlay_use_bgp,
)


class TestUnconfigureMdtOverlayUseBgp(unittest.TestCase):

    def test_unconfigure_mdt_overlay_use_bgp(self):
        device = Mock()

        result = unconfigure_mdt_overlay_use_bgp(
            device=device,
            vrf_name='vrf3001',
            address_family='ipv4',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'address-family ipv4',
                'no mdt overlay use-bgp',
            ]
        )
