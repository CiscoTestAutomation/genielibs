from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_cdp_run


class TestConfigureCdpRun(TestCase):

    def test_configure_cdp_run(self):
        device = Mock()
        result = configure_cdp_run(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('cdp run',)
        )