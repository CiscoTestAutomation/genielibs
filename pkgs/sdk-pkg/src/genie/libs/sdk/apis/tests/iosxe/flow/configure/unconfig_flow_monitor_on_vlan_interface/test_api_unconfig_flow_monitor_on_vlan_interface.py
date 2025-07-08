from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import unconfig_flow_monitor_on_vlan_interface
from unittest.mock import Mock


class TestUnconfigFlowMonitorOnVlanInterface(TestCase):

    def test_unconfig_flow_monitor_on_vlan_interface(self):
        self.device = Mock()
        result = unconfig_flow_monitor_on_vlan_interface(self.device, '100', 'ip', 'M2_input', 'input')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface vlan 100', 'no ip flow monitor M2_input input'],)
        )
