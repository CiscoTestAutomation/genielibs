from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_ipv6_logging_with_transport_and_facility
from unittest.mock import Mock


class TestConfigureIpv6LoggingWithTransportAndFacility(TestCase):

    def test_configure_ipv6_logging_with_transport_and_facility(self):
        self.device = Mock()
        result = configure_ipv6_logging_with_transport_and_facility(self.device, '2001::1:1', 'udp', '123')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no logging facility local0', 'no logging trap debugging', 'logging host ipv6 2001::1:1 transport udp port 123', 'no logging count'],)
        )
