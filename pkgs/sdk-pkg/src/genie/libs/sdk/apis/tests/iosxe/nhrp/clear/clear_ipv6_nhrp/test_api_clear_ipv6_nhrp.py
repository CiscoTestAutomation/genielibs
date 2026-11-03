import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nhrp.clear import (
    clear_ipv6_nhrp,
)


class TestClearIpv6Nhrp(TestCase):

    def test_clear_ipv6_nhrp(self):
        device = Mock()
        device.execute.return_value = None

        result = clear_ipv6_nhrp(device, False, False, False, None, 30)

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "clear ipv6 nhrp")
        device.execute.assert_called_once_with(
            command,
            error_pattern=[
                "VRF \"None\" is not valid.",
                r"% Invalid input detected at \'\^\' marker\.",
            ],
            timeout=30,
        )


if __name__ == "__main__":
    unittest.main()
