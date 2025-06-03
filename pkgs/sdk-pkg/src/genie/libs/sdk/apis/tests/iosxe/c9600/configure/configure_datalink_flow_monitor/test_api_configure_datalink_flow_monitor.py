from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9600.configure import configure_datalink_flow_monitor


class TestConfigureDatalinkFlowMonitor(TestCase):

    def test_configure_datalink_flow_monitor(self):
        self.device = Mock()
        result = configure_datalink_flow_monitor(self.device, 'Gi3/0/2', 'm2in1', 'input')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gi3/0/2', 'datalink flow monitor m2in1 input'],)
        )
