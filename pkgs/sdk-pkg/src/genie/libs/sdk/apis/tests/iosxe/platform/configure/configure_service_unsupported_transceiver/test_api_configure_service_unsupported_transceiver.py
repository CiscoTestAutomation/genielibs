from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_service_unsupported_transceiver
from unittest.mock import Mock


class TestConfigureServiceUnsupportedTransceiver(TestCase):

    def test_configure_service_unsupported_transceiver(self):
        self.device = Mock()
        result = configure_service_unsupported_transceiver(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('service unsupported-transceiver',)
        )
