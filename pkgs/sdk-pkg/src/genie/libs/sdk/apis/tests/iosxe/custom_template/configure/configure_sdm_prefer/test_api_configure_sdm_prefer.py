from unittest import TestCase
from genie.libs.sdk.apis.iosxe.custom_template.configure import configure_sdm_prefer
from unittest.mock import Mock


class TestConfigureSdmPrefer(TestCase):

    def test_configure_sdm_prefer(self):
        self.device = Mock()
        result = configure_sdm_prefer(self.device, 'access')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('sdm prefer access',)
        )

