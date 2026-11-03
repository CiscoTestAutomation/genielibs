import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_pim_bsr_candidate_bsr,
)


class TestConfigureIpv6PimBsrCandidateBsr(TestCase):

    def test_configure_ipv6_pim_bsr_candidate_bsr(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_pim_bsr_candidate_bsr(
            device,
            "61::61",
            "pim_1",
            10,
            5,
            100,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "ipv6 pim bsr candidate bsr 61::61 100 priority 10 scope 5 "
            "accept-rp-candidate pim_1",
        )


if __name__ == "__main__":
    unittest.main()
