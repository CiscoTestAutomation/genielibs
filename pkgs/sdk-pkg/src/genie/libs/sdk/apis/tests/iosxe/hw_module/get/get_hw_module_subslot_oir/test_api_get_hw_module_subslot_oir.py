import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.sdk.apis.iosxe.hw_module.get import (
    get_hw_module_subslot_oir,
)


class TestGetHwModuleSubslotOir(unittest.TestCase):

    def test_get_hw_module_subslot_oir(self):
        device = Mock()
        # Parsed 'show hw-module subslot 0/1 oir'
        parsed = {
            "subslots": {
                "0/1": {
                    "model": "C1127-ES-8",
                    "operational_status": "booting",
                }
            }
        }
        device.parse = Mock(return_value=parsed)

        result = get_hw_module_subslot_oir(device, "0/1")

        device.parse.assert_called_once_with(
            "show hw-module subslot 0/1 oir")
        self.assertEqual(result, parsed)

    def test_get_hw_module_subslot_oir_ok(self):
        device = Mock()
        parsed = {
            "subslots": {
                "0/1": {
                    "model": "C1127-ES-8",
                    "operational_status": "ok",
                }
            }
        }
        device.parse = Mock(return_value=parsed)

        result = get_hw_module_subslot_oir(device, "0/1")

        device.parse.assert_called_once_with(
            "show hw-module subslot 0/1 oir")
        self.assertEqual(result, parsed)

    def test_get_hw_module_subslot_oir_empty(self):
        device = Mock()
        device.parse = Mock(side_effect=SchemaEmptyParserError("empty"))

        result = get_hw_module_subslot_oir(device, "0/1")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
