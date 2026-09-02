import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    unconfigure_vlan_configuration,
)


class TestUnconfigureVlanConfiguration(unittest.TestCase):

    def test_unconfigure_vlan_configuration(self):
        device = Mock()

        result = unconfigure_vlan_configuration(device, 55)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no vlan configuration 55'
        )
