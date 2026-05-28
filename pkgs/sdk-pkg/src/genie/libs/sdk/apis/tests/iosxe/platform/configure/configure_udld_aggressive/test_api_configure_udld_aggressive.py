import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_udld_aggressive


class TestConfigureUdldAggressive(unittest.TestCase):

    def test_configure_udld_aggressive(self):
        device = Mock()

        result = configure_udld_aggressive(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('udld aggressive',)
        )