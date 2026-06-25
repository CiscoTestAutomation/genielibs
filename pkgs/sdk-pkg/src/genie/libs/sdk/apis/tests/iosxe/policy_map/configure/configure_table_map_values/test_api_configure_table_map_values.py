import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_table_map_values
)


class TestConfigureTableMapValues(unittest.TestCase):

    def test_configure_table_map_values(self):
        device = Mock()

        result = configure_table_map_values(
            device,
            't1',
            40,
            20
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['table-map t1',
              'map from 40 to 20'],)
        )