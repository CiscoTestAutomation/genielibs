import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_table_map_values
)


class TestUnconfigureTableMapValues(unittest.TestCase):

    def test_unconfigure_table_map_values(self):
        device = Mock()

        result = unconfigure_table_map_values(
            device,
            't1',
            40,
            20
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['table-map t1',
              'no map from 40 to 20'],)
        )