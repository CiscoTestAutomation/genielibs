import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_udld_port_aggressive


class TestConfigureUdldPortAggressive(unittest.TestCase):

    def test_configure_udld_port_aggressive(self):
        device = Mock()

        result = configure_udld_port_aggressive(device, 'Gig1/0/10')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Gig1/0/10', 'udld port aggressive'],)
        )