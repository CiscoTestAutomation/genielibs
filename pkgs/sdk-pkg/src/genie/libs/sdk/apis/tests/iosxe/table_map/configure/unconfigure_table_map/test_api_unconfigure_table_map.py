from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.table_map.configure import (
    unconfigure_table_map,
)


class TestUnconfigureTableMap(TestCase):

    def test_unconfigure_table_map(self):
        device = Mock()

        result = unconfigure_table_map(
            device=device,
            table_map_name='table_cos',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no table-map table_cos')
