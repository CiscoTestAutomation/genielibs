from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_stealthwatch_cloud_monitor
from unittest.mock import Mock


class TestConfigureStealthwatchCloudMonitor(TestCase):

    def test_configure_stealthwatch_cloud_monitor(self):
        self.device = Mock()
        result = configure_stealthwatch_cloud_monitor(self.device, 'cisco', 'cisco', 'https://sensor.eu-prod.obsrvbl.com')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['stealthwatch-cloud-monitor', ' sensor-name cisco', ' service-key cisco', ' url https://sensor.eu-prod.obsrvbl.com'],)
        )
