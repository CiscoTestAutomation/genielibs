from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    unconfigure_ipv6_nd_raguard_on_interface,
)


class TestUnconfigureIpv6NdRaguardOnInterface(TestCase):

    def test_unconfigure_ipv6_nd_raguard_on_interface(self):
        device = Mock()
        result = unconfigure_ipv6_nd_raguard_on_interface(
            device,
            'TwentyFiveGigE1/0/1',
        )
        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'interface TwentyFiveGigE1/0/1',
            'no ipv6 nd raguard',
        ])
