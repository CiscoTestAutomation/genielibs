from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import simulate_format_sdflash
from unittest.mock import Mock


class TestSimulateFormatSdflash(TestCase):

    def test_simulate_format_sdflash(self):
        self.device = Mock()
        results_map = {
            'format sdflash:': '''*Jul  8 09:47:01.206: %IOSD_INFRA-6-IFS_DEVICE_OIR: Device sdflash added
Format of sdflash: complete'''
        }

        # Use a side effect function that mimics device.execute
        def results_side_effect(command, **kwargs):
            return results_map.get(command, '')

        self.device.execute.side_effect = results_side_effect

        # Run the API
        result = simulate_format_sdflash(self.device)

        # Verify the command issued
        self.assertIn(
            'format sdflash:',
            self.device.execute.call_args_list[0][0]
        )

        expected_output = "Format of sdflash: complete"
        self.assertIn(expected_output, result)
