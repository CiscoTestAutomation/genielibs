import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_service_query_timer_periodicity,
)


class TestConfigureMdnsServiceQueryTimerPeriodicity(TestCase):

    def test_configure_mdns_service_query_timer_periodicity(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_service_query_timer_periodicity(device, 30)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "service-query-timer periodicity 30",
            ]
        )


if __name__ == "__main__":
    unittest.main()
