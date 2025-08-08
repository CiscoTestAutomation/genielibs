from unittest import TestCase
from genie.libs.sdk.apis.iosxe.custom_template.configure import configure_sdm_prefer_custom_template
from unittest.mock import Mock


class TestConfigureSdmPreferCustomTemplate(TestCase):

    def test_configure_sdm_prefer_custom_template(self):
        self.device = Mock()
        result = configure_sdm_prefer_custom_template(self.device,'acl', 'pbr', 27, 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['sdm prefer custom acl', 'pbr 27 priority 1'],)
        )

