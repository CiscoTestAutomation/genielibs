import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_switchport_trunk_allowed_vlan_except,
)


class TestConfigureSwitchportTrunkAllowedVlanExcept(unittest.TestCase):

    def test_configure_switchport_trunk_allowed_vlan_except(self):
        device = Mock()

        result = configure_switchport_trunk_allowed_vlan_except(
            device,
            'g1/1/1',
            '100',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface g1/1/1',
                'switchport trunk allowed vlan except 100',
            ]
        )
