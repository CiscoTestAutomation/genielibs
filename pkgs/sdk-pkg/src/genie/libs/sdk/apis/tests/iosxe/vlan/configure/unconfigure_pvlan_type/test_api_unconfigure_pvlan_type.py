import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_pvlan_type


class TestUnconfigurePvlanType(unittest.TestCase):

    def test_unconfigure_pvlan_type(self):
        device = Mock()

        result = unconfigure_pvlan_type(device, 2, 'isolated')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vlan 2',
                'no private-vlan isolated',
            ]
        )
