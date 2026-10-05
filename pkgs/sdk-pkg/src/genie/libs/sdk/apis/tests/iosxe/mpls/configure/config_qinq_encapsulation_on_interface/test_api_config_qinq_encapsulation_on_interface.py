import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mpls.configure import (
    config_qinq_encapsulation_on_interface,
)


class TestConfigQinqEncapsulationOnInterface(TestCase):

    def test_config_qinq_encapsulation_on_interface(self):
        device = Mock()
        device.configure.return_value = None

        result = config_qinq_encapsulation_on_interface(
            device,
            "10",
            "20",
            "gigabitethernet 0/0/1.10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "interface gigabitethernet 0/0/1.10",
                "encapsulation dot1q 10 second-dot1q 20",
            ]
        )


if __name__ == "__main__":
    unittest.main()
