from unittest import TestCase
from genie.libs.sdk.apis.iosxe.telemetry.configure import configure_product_analytics
from unittest.mock import Mock


class TestConfigureProductAnalytics(TestCase):

    def test_configure_product_analytics(self):
        self.device = Mock()
        result = configure_product_analytics(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('product-analytics',)
        )
