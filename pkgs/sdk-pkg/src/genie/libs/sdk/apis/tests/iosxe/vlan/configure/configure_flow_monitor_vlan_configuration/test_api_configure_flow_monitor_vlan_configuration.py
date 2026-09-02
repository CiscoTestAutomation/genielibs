from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_flow_monitor_vlan_configuration,
)


class TestConfigureFlowMonitorVlanConfiguration(TestCase):

    def test_configure_flow_monitor_vlan_configuration(self):
        device = Mock()

        result = configure_flow_monitor_vlan_configuration(
            device,
            vlan=100,
            monitor_name='fl_mon_Po',
            sampler_name='s4',
            direction='input',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vlan configuration 100',
                'ip flow monitor fl_mon_Po sampler s4 input',
            ]
        )
