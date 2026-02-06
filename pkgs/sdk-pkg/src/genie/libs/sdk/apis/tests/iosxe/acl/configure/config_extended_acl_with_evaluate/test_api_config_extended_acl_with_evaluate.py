from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import config_extended_acl_with_evaluate


class TestConfigExtendedAclWithEvaluate(TestCase):

    def test_config_extended_acl_with_evaluate(self):
        device = Mock()
        device.configure.return_value = ""

        result = config_extended_acl_with_evaluate(device, "test1", None)
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "ip access-list extended test1",
                "evaluate None",
            ],)
        )