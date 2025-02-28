from unittest import TestCase
from genie.libs.sdk.apis.iosxe.span.configure import configure_remote_span_on_vlan
from unittest.mock import Mock


class TestConfigureRemoteSpanOnVlan(TestCase):

    def test_configure_remote_span_on_vlan(self):
        self.device = Mock()
        result = configure_remote_span_on_vlan(self.device, '501')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vlan 501', 'remote-span'],)
        )
