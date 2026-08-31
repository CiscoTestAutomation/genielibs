import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import unconfigure_default_vxlan


class TestUnconfigureDefaultVxlan(unittest.TestCase):

    def test_unconfigure_default_vxlan(self):
        device = Mock()

        result = unconfigure_default_vxlan(
            device,
            'green',
            'ipv4',
            '239.1.1.1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vrf definition green',
                'address-family ipv4',
                'no mdt default vxlan  239.1.1.1',
            ]
        )
