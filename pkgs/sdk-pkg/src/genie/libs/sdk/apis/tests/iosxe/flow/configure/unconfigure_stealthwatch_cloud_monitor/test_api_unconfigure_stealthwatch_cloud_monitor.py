from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_stealthwatch_cloud_monitor
from unittest.mock import Mock


class TestUnconfigureStealthwatchCloudMonitor(TestCase):

    def test_unconfigure_stealthwatch_cloud_monitor(self):
        self.device = Mock()
        result = unconfigure_stealthwatch_cloud_monitor(self.device, 'cisco', 'cisco', 'https://sensor.eu-prod.obsrvbl.com')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['stealthwatch-cloud-monitor', 'no sensor-name cisco', 'no service-key cisco', 'no url https://sensor.eu-prod.obsrvbl.com'],)
        )
