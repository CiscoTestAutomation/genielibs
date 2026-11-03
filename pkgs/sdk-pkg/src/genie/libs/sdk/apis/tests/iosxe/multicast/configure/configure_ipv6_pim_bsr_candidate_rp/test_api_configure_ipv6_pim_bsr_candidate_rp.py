import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_pim_bsr_candidate_rp,
)


class TestConfigureIpv6PimBsrCandidateRp(TestCase):

    def test_configure_ipv6_pim_bsr_candidate_rp(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_pim_bsr_candidate_rp(
            device,
            "61::61",
            "list1",
            None,
            None,
            None,
            True,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "ipv6 pim bsr candidate rp 61::61 group-list list1 bidir",
        )


if __name__ == "__main__":
    unittest.main()
