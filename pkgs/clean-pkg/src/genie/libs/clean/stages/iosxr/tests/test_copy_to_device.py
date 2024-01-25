import unittest
from unittest.mock import Mock, call, ANY

from random import randint

from genie.libs.clean.stages.stages import CopyToDevice
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed
from pyats.topology import Testbed
from pyats.datastructures import AttrDict


class VerifyCopyToDevice(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = CopyToDevice()
        self.cls.history = {'CopyToDevice': AttrDict({'parameters': {}})}

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxr')

    def test_copy_to_device(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:': iter([
                    '''
                        Directory of bootflash:/
                        260234 -rw-rw-rw-. 1 1234 Dec  4 11:25 ds_stats.txt
                        260207 drwx------. 2 4096 Nov 30 20:46 repodata
                        6961520 kbytes total (2014552 kbytes free)
                    ''',
                    f'''
                        Directory of bootflash:/
                        260234 -rw-rw-rw-. 1 1234 Dec  4 11:25 ds_stats.txt
                        260155 -rw-rw-rw-. 1 4096 Dec  4 11:30 test.bin
                        260207 drwx------. 2 4096 Nov 30 20:46 repodata
                        6961520 kbytes total (2014552 kbytes free)
                    '''
                    ]),
                    'copy http://127.0.0.1//path/test.bin bootflash:/test.bin': iter(['Successfully copied']),
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed('mytb', servers={
            'server1': {
                'address': '127.0.0.1',
                'protocol': 'http'
            }
        })

        self.device.testbed = testbed

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(
            steps=steps, device=self.device,
            origin=dict(
                files=[f'/path/test.bin'],
                hostname='server1'
            ),
            destination=dict(
                directory='bootflash:'
            ),
            protocol='http',
            verify_running_image=False
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy http://127.0.0.1//path/test.bin bootflash:/test.bin',
                 prompt_recovery=False, timeout=300, reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])


    def test_copy_to_device_long_filename(self):
        filler = 'a' * 125

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:': iter([
                    '''
                        Directory of bootflash:/
                        260234 -rw-rw-rw-. 1 1234 Dec  4 11:25 ds_stats.txt
                        260207 drwx------. 2 4096 Nov 30 20:46 repodata
                        6961520 kbytes total (2014552 kbytes free)
                    ''',
                    f'''
                        Directory of bootflash:/
                        260234 -rw-rw-rw-. 1 1234 Dec  4 11:25 ds_stats.txt
                        260155 -rw-rw-rw-. 1 4096 Dec  4 11:30 {filler}test.bin
                        260207 drwx------. 2 4096 Nov 30 20:46 repodata
                        6961520 kbytes total (2014552 kbytes free)
                    '''
                    ]),
                    f'copy http://127.0.0.1//path/{filler}test.bin bootflash:/{filler}test.bin': iter(['Successfully copied'])
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed('mytb', servers={
            'server1': {
                'address': '127.0.0.1',
                'protocol': 'http'
            }
        })

        self.device.testbed = testbed

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(
            steps=steps, device=self.device,
            origin=dict(
                files=[f'/path/{filler}test.bin'],
                hostname='server1'
            ),
            destination=dict(
                directory='bootflash:'
            ),
            protocol='http',
            verify_running_image=False
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy http://127.0.0.1//path/{filler}test.bin bootflash:/{filler}test.bin',
                 prompt_recovery=False, timeout=300, reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_unique_file_name(self):
        unique_number = randint(1, 100)

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:': iter([
                    '''
                        Directory of bootflash:/
                        260234 -rw-rw-rw-. 1 1234 Dec  4 11:25 ds_stats.txt
                        260207 drwx------. 2 4096 Nov 30 20:46 repodata
                        6961520 kbytes total (2014552 kbytes free)
                    ''',
                    f'''
                        Directory of bootflash:/
                        260234 -rw-rw-rw-. 1 1234 Dec  4 11:25 ds_stats.txt
                        260155 -rw-rw-rw-. 1 4096 Dec  4 11:30 test_{unique_number}.bin
                        260207 drwx------. 2 4096 Nov 30 20:46 repodata
                        6961520 kbytes total (2014552 kbytes free)
                    '''
                    ]),
                    f'copy http://127.0.0.1//path/test.bin bootflash:/test_{unique_number}.bin': iter(['Successfully copied'])
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed('mytb', servers={
            'server1': {
                'address': '127.0.0.1',
                'protocol': 'http'
            }
        })

        self.device.testbed = testbed

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(
            steps=steps, device=self.device,
            origin=dict(
                files=[f'/path/test.bin'],
                hostname='server1'
            ),
            destination=dict(
                directory='bootflash:'
            ),
            protocol='http',
            unique_file_name=True,
            unique_number=unique_number,
            verify_running_image=False
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy http://127.0.0.1//path/test.bin bootflash:/test_{unique_number}.bin',
                 prompt_recovery=False, timeout=300, reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_rename_images(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:': iter([
                    '''
                        Directory of bootflash:/
                        260234 -rw-rw-rw-. 1 1234 Dec  4 11:25 ds_stats.txt
                        260207 drwx------. 2 4096 Nov 30 20:46 repodata
                        6961520 kbytes total (2014552 kbytes free)
                    ''',
                    '''
                        Directory of bootflash:/
                        260234 -rw-rw-rw-. 1 1234 Dec  4 11:25 ds_stats.txt
                        260155 -rw-rw-rw-. 1 4096 Dec  4 11:30 test.bin_0
                        260207 drwx------. 2 4096 Nov 30 20:46 repodata
                        6961520 kbytes total (2014552 kbytes free)
                    '''
                    ]),
                    'copy http://127.0.0.1//my/test.bin bootflash:': iter(['']),
                    f'copy http://127.0.0.1//path/test.bin bootflash:/test.bin_0': iter(['Successfully copied'])
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed('mytb', servers={
            'server1': {
                'address': '127.0.0.1',
                'protocol': 'http'
            }
        })

        self.device.testbed = testbed

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(
            steps=steps, device=self.device,
            origin=dict(
                files=[f'/path/test.bin'],
                hostname='server1'
            ),
            destination=dict(
                directory='bootflash:'
            ),
            protocol='http',
            rename_images='test.bin',
            verify_running_image=False
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy http://127.0.0.1//path/test.bin bootflash:/test.bin_0',
                 prompt_recovery=False, timeout=300, reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])
