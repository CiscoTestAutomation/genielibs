from unittest import TestCase
from genie.libs.sdk.apis.iosxe.stack.utils import free_up_disk_space
from unittest.mock import ANY, Mock, call


class TestFreeUpDiskSpace(TestCase):

    def test_free_up_disk_space(self):
        self.device = Mock()
        destination= 'bootflash'
        protect_files = ['image.bin']
        dir_parse ={'dir': {'dir': 'flash:/',
                         'flash:/': {'bytes_free': '494469120',
                                    'bytes_total': '11353194496',
                                    'files': {
                                        'old-image.bin': {
                                            'permissions': '-rw-',
                                            'size': '4096'},
                                        'core': {
                                            'permissions': 'drwx',
                                            'size': '2048'},
                                        'crashinfo': {
                                            'permissions': 'drwx',
                                            'size': '4096'}}}}}
        self.device.api.get_available_space = Mock(return_value= 100)
        self.device.api.get_running_image = Mock(return_value=[])
        self.device.api.verify_enough_disk_space = Mock(
            side_effect=[False, False, False, True])
        self.device.api.delete_unprotected_files = Mock()
        self.device.parse = Mock(return_value=dir_parse)
        dir_out= 'out'
        
        free_up_disk_space(self.device, destination=destination,
                           required_size=110, skip_deletion=False,
                           protected_files=protect_files, dir_output=dir_out)
        
        self.device.api.delete_unprotected_files.assert_has_calls([
            call(directory='bootflash', protected={'image.bin'},
                 files_to_delete=['crashinfo'], dir_output='out',
                 allow_failure=False, destination='bootflash',
                 recursive=True, stop_check=ANY),
            call(directory='bootflash', protected={'image.bin'},
                 files_to_delete=['core'], dir_output='out',
                 allow_failure=False, destination='bootflash',
                 recursive=True, stop_check=ANY),
            call(directory='bootflash', protected={'image.bin'},
                 files_to_delete=['old-image.bin'], dir_output='out',
                 allow_failure=False, destination='bootflash')])
        self.assertEqual(self.device.api.delete_unprotected_files.call_count, 3)

    def test_free_up_disk_space_stops_after_directory_cleanup(self):
        self.device = Mock()
        destination = 'bootflash'
        protect_files = ['image.bin']
        dir_parse = {'dir': {'dir': 'flash:/',
                             'flash:/': {'bytes_free': '494469120',
                                         'bytes_total': '11353194496',
                                         'files': {
                                             'old-image.bin': {
                                                 'permissions': '-rw-',
                                                 'size': '4096'},
                                             'core': {
                                                 'permissions': 'drwx',
                                                 'size': '2048'},
                                             'crashinfo': {
                                                 'permissions': 'drwx',
                                                 'size': '4096'}}}}}
        self.device.api.get_available_space = Mock(return_value=100)
        self.device.api.get_running_image = Mock(return_value=[])
        self.device.api.verify_enough_disk_space = Mock(
            side_effect=[False, True])
        self.device.api.delete_unprotected_files = Mock()
        self.device.parse = Mock(return_value=dir_parse)
        dir_out = 'out'

        free_up_disk_space(self.device, destination=destination,
                           required_size=110, skip_deletion=False,
                           protected_files=protect_files, dir_output=dir_out)

        self.device.api.delete_unprotected_files.assert_called_once_with(
            directory='bootflash', protected={'image.bin'},
            files_to_delete=['crashinfo'], dir_output='out',
            allow_failure=False, destination='bootflash',
            recursive=True, stop_check=ANY)
