from unittest import TestCase
from unittest.mock import MagicMock

from genie.libs.sdk.apis.verify import verify_enough_disk_space


class TestVerifyEnoughDiskSpace(TestCase):

    def test_unknown_space_is_not_sufficient(self):
        device = MagicMock()
        device.api.get_available_space.return_value = None

        self.assertFalse(verify_enough_disk_space(
            device,
            required_size=-1,
            directory='bootflash:/',
            dir_output='malformed output',
        ))

    def test_known_zero_space_remains_distinct_from_unknown(self):
        device = MagicMock()
        device.api.get_available_space.return_value = 0

        self.assertTrue(verify_enough_disk_space(
            device,
            required_size=-1,
            directory='bootflash:/',
            dir_output='valid output',
        ))
