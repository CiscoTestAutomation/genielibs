from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_tracking_object
from unittest.mock import Mock


class TestConfigureTrackingObject(TestCase):

    def test_configure_tracking_object(self):
        self.device = Mock()
        result = configure_tracking_object(self.device, '301', 'Vlan301', 'line-protocol', 'up', 180)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['track 301 interface Vlan301 line-protocol', 'delay up 180'],)
        )
