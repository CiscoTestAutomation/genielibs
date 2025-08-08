from unittest import TestCase
from genie.libs.sdk.apis.iosxe.custom_template.configure import configure_sdm_prefer_core
from unittest.mock import Mock


class TestConfigureSdmPreferCore(TestCase):

    def test_configure_sdm_prefer_core(self):
        self.device = Mock()
        result = configure_sdm_prefer_core(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['sdm prefer core'],)
        )

