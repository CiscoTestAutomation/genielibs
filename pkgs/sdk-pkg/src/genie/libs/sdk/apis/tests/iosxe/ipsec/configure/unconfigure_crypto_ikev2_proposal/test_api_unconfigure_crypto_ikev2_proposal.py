import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    unconfigure_crypto_ikev2_proposal,
)


class TestUnconfigureCryptoIkev2Proposal(TestCase):

    def test_unconfigure_crypto_ikev2_proposal(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_crypto_ikev2_proposal(device, "newproposal")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no crypto ikev2 proposal newproposal"],
        )


if __name__ == "__main__":
    unittest.main()
