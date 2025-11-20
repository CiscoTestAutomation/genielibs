from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import execute_set_config_register
from unittest.mock import Mock


class TestExecuteSetConfigRegister(TestCase):
    def test_execute_set_config_register(self):
        self.device = Mock()
        result = execute_set_config_register(self.device, config_register='0x2102', timeout=10)
        self.assertEqual(result, None)

