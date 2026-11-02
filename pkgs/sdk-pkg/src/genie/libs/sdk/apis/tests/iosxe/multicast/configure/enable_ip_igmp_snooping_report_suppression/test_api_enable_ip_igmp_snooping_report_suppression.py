import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    enable_ip_igmp_snooping_report_suppression,
)


class TestEnableIpIgmpSnoopingReportSuppression(TestCase):

    def test_enable_ip_igmp_snooping_report_suppression(self):
        device = Mock()
        device.configure.return_value = None

        result = enable_ip_igmp_snooping_report_suppression(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "ip igmp snooping report-suppression")


if __name__ == "__main__":
    unittest.main()
