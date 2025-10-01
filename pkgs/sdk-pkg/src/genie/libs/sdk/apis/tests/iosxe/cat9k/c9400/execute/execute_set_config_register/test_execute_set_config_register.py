from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cat9k.c9400.execute import execute_set_config_register
from unittest.mock import Mock


class TestExecuteSetConfigRegister(TestCase):

    def test_execute_set_config_register(self):
        self.device = Mock()
        self.device.subconnections = None
        results_map = {
            'boot manual': '',
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.configure.side_effect = results_side_effect

        result = execute_set_config_register(self.device,'0x0', 300)

        self.assertIn(
            'boot manual',
            self.device.default.configure.call_args_list[0][0]
        )
        expected_cmd = f'boot manual'
        expected_output = None
        self.assertEqual(result, expected_output)
