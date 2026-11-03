import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.bgp.clear import (
    clear_bgp_all_as,
)


class TestClearBgpAllAs(TestCase):

    def test_clear_bgp_all_as(self):
        device = Mock()
        device.execute.return_value = None

        result = clear_bgp_all_as(device, 100)

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "clear bgp all 100")
        device.execute.assert_called_once_with(command)


if __name__ == "__main__":
    unittest.main()
