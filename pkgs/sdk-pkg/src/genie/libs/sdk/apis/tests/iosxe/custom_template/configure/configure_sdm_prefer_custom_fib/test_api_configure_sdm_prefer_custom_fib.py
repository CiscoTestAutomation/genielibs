from unittest import TestCase
from genie.libs.sdk.apis.iosxe.custom_template.configure import configure_sdm_prefer_custom_fib
from unittest.mock import Mock


class TestConfigureSdmPreferCustomFib(TestCase):

    def test_configure_sdm_prefer_custom_fib(self):
        self.device = Mock()
        result = configure_sdm_prefer_custom_fib(self.device,'mac-address', '16', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['sdm prefer custom fib', 'mac-address 16 priority 1'],)
        )

