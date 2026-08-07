import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    unconfigure_crypto_transform_set,
)


class TestUnconfigureCryptoTransformSet(TestCase):

    def test_unconfigure_crypto_transform_set(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_crypto_transform_set(
            device,
            "test_transform_name",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no crypto ipsec transform-set test_transform_name"],
        )


if __name__ == "__main__":
    unittest.main()
