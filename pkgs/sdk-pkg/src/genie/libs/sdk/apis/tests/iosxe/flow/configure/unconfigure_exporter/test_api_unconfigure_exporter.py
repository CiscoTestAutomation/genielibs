from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_exporter
from unittest.mock import Mock


class TestUnconfigureExporter(TestCase):

    def test_unconfigure_exporter(self):
        self.device = Mock()
        result = unconfigure_exporter(self.device, 'exporter1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no flow exporter exporter1'],)
        )
