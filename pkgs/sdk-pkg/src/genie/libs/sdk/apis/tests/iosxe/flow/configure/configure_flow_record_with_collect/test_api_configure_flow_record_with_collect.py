from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_record_with_collect
from unittest.mock import Mock


class TestConfigureFlowRecordWithCollect(TestCase):

    def test_configure_flow_record_with_collect(self):
        self.device = Mock()
        result = configure_flow_record_with_collect(self.device, 'A', 'record A', ['connection', 'server', 'counter', 'packets', 'long'])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow record A', 'description record A', 'collect connection server counter packets long'],)
        )
