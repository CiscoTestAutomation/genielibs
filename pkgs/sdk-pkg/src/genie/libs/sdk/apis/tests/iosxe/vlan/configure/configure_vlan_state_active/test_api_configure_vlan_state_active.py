import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vlan_state_active


class TestConfigureVlanStateActive(unittest.TestCase):

    def test_configure_vlan_state_active(self):
        device = Mock()

        result = configure_vlan_state_active(
            device,
            'Te3/1/8',
            '100',
            'active',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface Te3/1/8',
                'vlan 100',
                'state active',
            ]
        )
