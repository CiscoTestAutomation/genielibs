import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nhrp.clear import (
    clear_ip_nhrp,
)


class TestClearIpNhrp(TestCase):

    def test_clear_ip_nhrp(self):
        device = Mock()
        device.execute.return_value = None

        result = clear_ip_nhrp(device, False, False, True, None, 30)

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "clear ip nhrp stats")
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
