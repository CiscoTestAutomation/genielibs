import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    unconfigure_ip_igmp_querier_query_interval,
)


class TestUnconfigureIpIgmpQuerierQueryInterval(TestCase):

    def test_unconfigure_ip_igmp_querier_query_interval(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_igmp_querier_query_interval(
            device,
            "query-interval",
            "100",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn(
            "no ip igmp snooping querier query-interval 100",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()