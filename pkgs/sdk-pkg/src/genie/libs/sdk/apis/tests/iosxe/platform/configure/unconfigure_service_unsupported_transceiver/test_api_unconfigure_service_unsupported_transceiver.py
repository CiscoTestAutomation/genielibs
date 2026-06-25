from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_service_unsupported_transceiver
from unittest.mock import Mock


class TestUnconfigureServiceUnsupportedTransceiver(TestCase):

    def test_unconfigure_service_unsupported_transceiver(self):
        self.device = Mock()
        result = unconfigure_service_unsupported_transceiver(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no service unsupported-transceiver',)
        )
