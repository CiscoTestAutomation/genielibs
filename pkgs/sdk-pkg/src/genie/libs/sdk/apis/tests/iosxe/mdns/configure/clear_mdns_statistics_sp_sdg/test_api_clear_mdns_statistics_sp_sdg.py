import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    clear_mdns_statistics_sp_sdg,
)


class TestClearMdnsStatisticsSpSdg(TestCase):

    def test_clear_mdns_statistics_sp_sdg(self):
        device = Mock()
        device.execute.return_value = None

        result = clear_mdns_statistics_sp_sdg(device)

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            "clear mdns-sd sp-sdg statistics"
        )


if __name__ == "__main__":
    unittest.main()
