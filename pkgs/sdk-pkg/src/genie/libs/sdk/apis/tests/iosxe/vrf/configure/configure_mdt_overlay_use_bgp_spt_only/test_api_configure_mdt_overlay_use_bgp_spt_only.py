import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_mdt_overlay_use_bgp_spt_only,
)


class TestConfigureMdtOverlayUseBgpSptOnly(unittest.TestCase):

    def test_configure_mdt_overlay_use_bgp_spt_only(self):
        device = Mock()

        result = configure_mdt_overlay_use_bgp_spt_only(
            device,
            'green',
            'ipv4',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition green',
                'address-family ipv4',
                'mdt overlay use-bgp spt-only',
            ]
        )
