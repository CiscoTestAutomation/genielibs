import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_vlan_state_suspend,
)


class TestConfigureVlanStateSuspend(unittest.TestCase):

    def test_configure_vlan_state_suspend(self):
        device = Mock()

        result = configure_vlan_state_suspend(
            device,
            'Te3/1/8',
            '100',
            'suspend',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface Te3/1/8',
                'vlan 100',
                'state suspend',
            ]
        )
