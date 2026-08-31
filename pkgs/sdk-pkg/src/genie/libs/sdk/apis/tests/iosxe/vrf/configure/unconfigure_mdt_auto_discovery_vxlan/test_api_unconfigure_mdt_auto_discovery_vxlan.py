import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    unconfigure_mdt_auto_discovery_vxlan,
)


class TestUnconfigureMdtAutoDiscoveryVxlan(unittest.TestCase):

    def test_unconfigure_mdt_auto_discovery_vxlan(self):
        device = Mock()

        result = unconfigure_mdt_auto_discovery_vxlan(
            device,
            'vrf3001',
            'ipv4',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition vrf3001',
                'address-family ipv4',
                'no mdt auto-discovery vxlan',
            ]
        )
