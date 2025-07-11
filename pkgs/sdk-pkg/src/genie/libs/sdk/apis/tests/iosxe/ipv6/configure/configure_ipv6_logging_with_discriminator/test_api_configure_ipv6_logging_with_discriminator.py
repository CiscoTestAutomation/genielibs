from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_ipv6_logging_with_discriminator
from unittest.mock import Mock


class TestConfigureIpv6LoggingWithDiscriminator(TestCase):

    def test_configure_ipv6_logging_with_discriminator(self):
        self.device = Mock()
        result = configure_ipv6_logging_with_discriminator(self.device, '2001::1:1', 'engCAsps', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['logging host ipv6 2001::1:1 discriminator engCAsps', 'logging count'],)
        )
