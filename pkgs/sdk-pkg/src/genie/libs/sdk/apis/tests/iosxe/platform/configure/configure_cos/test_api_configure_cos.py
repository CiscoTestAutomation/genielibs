from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_cos


class TestConfigureCos(TestCase):

    def test_configure_cos(self):
        device = Mock()
        result = configure_cos(
            device,
            5
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['l2protocol-tunnel cos 5'],)
        )