from unittest import TestCase
from genie.libs.sdk.apis.iosxe.telemetry.configure import unconfigure_product_analytics
from unittest.mock import Mock


class TestUnconfigureProductAnalytics(TestCase):

    def test_unconfigure_product_analytics(self):
        self.device = Mock()
        result = unconfigure_product_analytics(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no product-analytics',)
        )
