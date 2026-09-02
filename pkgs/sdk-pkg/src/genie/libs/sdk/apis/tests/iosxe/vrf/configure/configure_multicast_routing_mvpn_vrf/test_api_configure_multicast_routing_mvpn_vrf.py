import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_multicast_routing_mvpn_vrf,
)


class TestConfigureMulticastRoutingMvpnVrf(unittest.TestCase):

    def test_configure_multicast_routing_mvpn_vrf(self):
        device = Mock()

        result = configure_multicast_routing_mvpn_vrf(
            device=device,
            vrf='vrf3001',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'ip multicast-routing vrf vrf3001'
        )
