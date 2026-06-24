import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_process_cpu_statistics_limit_entry_percentage_size


class TestUnconfigureProcessCpuStatisticsLimitEntryPercentageSize(unittest.TestCase):

    def test_unconfigure_process_cpu_statistics_limit_entry_percentage_size(self):
        device = Mock()

        result = unconfigure_process_cpu_statistics_limit_entry_percentage_size(
            device,
            '10',
            '100'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no process cpu  statistics limit entry-percentage 10 size 100',)
        )