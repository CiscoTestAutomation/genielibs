import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import clear_mdns_statistics_all


class TestClearMdnsStatisticsAll(TestCase):

    def test_clear_mdns_statistics_all(self):
        device = Mock()
        device.execute.return_value = None

        result = clear_mdns_statistics_all(device)

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            "clear mdns-sd statistics all"
        )


if __name__ == "__main__":
    unittest.main()
