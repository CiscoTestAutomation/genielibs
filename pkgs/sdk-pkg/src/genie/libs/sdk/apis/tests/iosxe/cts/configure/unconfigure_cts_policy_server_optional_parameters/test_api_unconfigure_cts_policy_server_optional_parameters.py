from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cts.configure import (
    unconfigure_cts_policy_server_optional_parameters,
)

class TestUnconfigureCtsPolicyServerOptionalParameters(TestCase):

    def test_unconfigure_cts_policy_server_optional_parameters(self):
        device = Mock()

        unconfigure_cts_policy_server_optional_parameters(
            device=device,
            server_name="ISE-server",
        )

        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    "cts policy-server name ISE-server",
                    "no retransmit",
                    "no timeout",
                    "no content-type json",
                ],
            ),
        )
