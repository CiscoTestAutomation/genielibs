import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    unconfigure_ip_vrf_forwarding_interface,
)


class TestUnconfigureIpVrfForwardingInterface(unittest.TestCase):

    def test_unconfigure_ip_vrf_forwarding_interface(self):
        device = Mock()

        result = unconfigure_ip_vrf_forwarding_interface(
            device,
            'te0/1/0',
            'test',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface te0/1/0',
                'no ip vrf forwarding test',
            ]
        )
