from unittest import TestCase
from genie.libs.sdk.apis.iosxe.span.configure import configure_source_destination_remote_vlan
from unittest.mock import Mock


class TestConfigureSourceDestinationRemoteVlan(TestCase):

    def test_configure_source_destination_remote_vlan(self):
        self.device = Mock()
        result = configure_source_destination_remote_vlan(self.device, 1, 'source', '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('monitor session 1 source remote vlan 100\n',)
        )
