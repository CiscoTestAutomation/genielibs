from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.execute import execute_crypto_pki_certificate_validate
from unittest.mock import Mock


class TestExecuteCryptoPkiCertificateValidate(TestCase):

    def test_execute_crypto_pki_certificate_validate(self):
        self.device = Mock()
        results_map = {
            "crypto pki certificate validate root": "Validation Failed: trustpoint not found for root",
        }

        def results_side_effect(arg, **kwargs):
            if isinstance(arg, (list, tuple)):
                arg = " ".join(arg)
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_crypto_pki_certificate_validate(self.device, "root")

        executed_cmd_arg = self.device.execute.call_args_list[0][0][0]
        if isinstance(executed_cmd_arg, list):
            executed_cmd = " ".join(executed_cmd_arg)
        else:
            executed_cmd = str(executed_cmd_arg)

        self.assertIn("crypto pki certificate validate root", executed_cmd)

        expected_output = None
        self.assertEqual(result, expected_output)
