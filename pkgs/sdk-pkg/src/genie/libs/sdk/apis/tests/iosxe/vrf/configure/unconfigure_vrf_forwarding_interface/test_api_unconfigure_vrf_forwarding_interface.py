import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    unconfigure_vrf_forwarding_interface,
)


class TestUnconfigureVrfForwardingInterface(unittest.TestCase):

    def test_unconfigure_vrf_forwarding_interface(self):
        device = Mock()

        result = unconfigure_vrf_forwarding_interface(
            device,
            'vlan1006',
            'vrf1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface vlan1006',
                'no vrf forwarding vrf1',
            ]
        )
