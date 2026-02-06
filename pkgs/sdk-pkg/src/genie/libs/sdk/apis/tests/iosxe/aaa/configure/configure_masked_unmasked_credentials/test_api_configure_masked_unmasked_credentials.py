from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_masked_unmasked_credentials


class TestConfigureMaskedUnmaskedCredentials(TestCase):

    def test_configure_masked_unmasked_credentials(self):
        device = Mock()
        device.configure.return_value = ""  

        result = configure_masked_unmasked_credentials(
            device, "USER", "test", 15, "POLICY", None, False, True, "VIEW"
        )
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ("username USER privilege 15 view VIEW common-criteria-policy POLICY secret test",)
        )