import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    configure_system_jumbomtu
)


class TestConfigureSystemJumbomtu(unittest.TestCase):

    def test_configure_system_jumbomtu(self):
        device = Mock()

        result = configure_system_jumbomtu(
            device,
            1900
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('system jumbomtu 1900',)
        )