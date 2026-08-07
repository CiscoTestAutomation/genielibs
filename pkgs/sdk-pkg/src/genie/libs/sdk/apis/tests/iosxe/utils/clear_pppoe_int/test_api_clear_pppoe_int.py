from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.utils import clear_pppoe_int


class TestClearPppoeInt(TestCase):

    def test_clear_pppoe_int(self):
        device = Mock()

        result = clear_pppoe_int(device, "Ethernet1/0.100")

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear pppoe int Ethernet1/0.100",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)

    def test_clear_pppoe_int_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            clear_pppoe_int(device, "Ethernet1/0.100")
