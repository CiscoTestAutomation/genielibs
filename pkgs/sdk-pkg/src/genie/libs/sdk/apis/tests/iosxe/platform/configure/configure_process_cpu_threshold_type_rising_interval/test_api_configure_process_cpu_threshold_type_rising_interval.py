import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_process_cpu_threshold_type_rising_interval


class TestConfigureProcessCpuThresholdTypeRisingInterval(unittest.TestCase):

    def test_configure_process_cpu_threshold_type_rising_interval(self):
        device = Mock()

        result = configure_process_cpu_threshold_type_rising_interval(device, 'total', '6', '5')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('process cpu threshold type total rising 6 interval 5',)
        )