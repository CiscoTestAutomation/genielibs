from unittest import TestCase
from unittest.mock import Mock, patch

from genie.libs.sdk.apis.iosxe.dual_rp.utils import free_up_disk_space


class TestFreeUpDiskSpace(TestCase):

    @patch(
        'genie.libs.sdk.apis.iosxe.dual_rp.utils.'
        'multi_rp_free_up_disk_space')
    def test_free_up_disk_space_forwards_optional_arguments(
            self, multi_rp_free_up_disk_space):
        device = Mock()
        protected_files = {
            'bootflash:': ['image.bin', 'packages.conf'],
            'stby-bootflash:': ['image.bin', 'packages.conf'],
        }
        multi_rp_free_up_disk_space.return_value = True

        result = free_up_disk_space(
            device,
            destination=['bootflash:', 'stby-bootflash:'],
            required_size=100,
            skip_deletion=False,
            protected_files=protected_files,
            compact=True,
            min_free_space_percent=20,
            dir_output='dir output',
            allow_deletion_failure=True)

        self.assertTrue(result)
        multi_rp_free_up_disk_space.assert_called_once_with(
            device,
            ['bootflash:', 'stby-bootflash:'],
            100,
            False,
            protected_files,
            compact=True,
            min_free_space_percent=20,
            dir_output='dir output',
            allow_deletion_failure=True)
