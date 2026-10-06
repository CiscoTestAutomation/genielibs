from unittest import TestCase
from unittest.mock import Mock, call, patch

from genie.libs.sdk.apis.iosxe.stack.utils import free_up_disk_space
from genie.libs.sdk.apis.iosxe.utils import _IOSXE_DISK_CLEANUP_STRATEGY


class TestFreeUpDiskSpace(TestCase):

    @patch('genie.libs.sdk.apis.iosxe.stack.utils._free_up_disk_space_with_strategy')
    def test_delegates_each_destination_to_shared_cleanup(
            self, shared_free_up_disk_space):
        device = Mock()
        protected_files = {
            'bootflash:': ['active.bin'],
            'flash-2:': ['active.bin', 'member-two.pkg'],
        }
        dir_output = {
            'bootflash:': 'active dir output',
            'flash-2:': 'member two dir output',
        }
        shared_free_up_disk_space.return_value = True

        result = free_up_disk_space(
            device=device,
            destination=['bootflash:', 'flash-2:'],
            required_size=110,
            skip_deletion=False,
            protected_files=protected_files,
            compact=True,
            min_free_space_percent=20,
            dir_output=dir_output,
            allow_deletion_failure=True,
        )

        self.assertTrue(result)
        shared_free_up_disk_space.assert_has_calls([
            call(
                device=device,
                destination='bootflash:',
                required_size=110,
                skip_deletion=False,
                protected_files=['active.bin'],
                compact=True,
                min_free_space_percent=20,
                dir_output='active dir output',
                allow_deletion_failure=True,
                recursive=True,
                cleanup_strategy=_IOSXE_DISK_CLEANUP_STRATEGY,
            ),
            call(
                device=device,
                destination='flash-2:',
                required_size=110,
                skip_deletion=False,
                protected_files=['active.bin', 'member-two.pkg'],
                compact=True,
                min_free_space_percent=20,
                dir_output='member two dir output',
                allow_deletion_failure=True,
                recursive=True,
                cleanup_strategy=_IOSXE_DISK_CLEANUP_STRATEGY,
            ),
        ])

    @patch('genie.libs.sdk.apis.iosxe.stack.utils._free_up_disk_space_with_strategy')
    def test_stops_when_a_member_cannot_verify_space(
            self, shared_free_up_disk_space):
        shared_free_up_disk_space.side_effect = [True, False, True]
        device = Mock()

        result = free_up_disk_space(
            device=device,
            destination=['bootflash:', 'flash-2:', 'flash-3:'],
            required_size=110,
            skip_deletion=False,
            protected_files=['active.bin'],
            dir_output='shared output',
        )

        self.assertFalse(result)
        self.assertEqual(shared_free_up_disk_space.call_count, 2)
