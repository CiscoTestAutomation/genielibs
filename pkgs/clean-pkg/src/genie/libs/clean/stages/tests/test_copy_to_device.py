import unittest

from unittest.mock import Mock, call, ANY

from genie.libs.clean.stages.stages import CopyToDevice
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from pyats.topology import Testbed
from pyats.datastructures import AttrDict


class VerifyCopyToDevice(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = CopyToDevice()
        self.cls.history = {'CopyToDevice': AttrDict({'parameters': {}})}

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_copy_to_device(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:': iter([
                    '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''',
                    f'''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  test.bin
                                1940303872 bytes total (1036210176 bytes free)
                    '''
                    ]),
                    'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin': iter(['Copied file']),
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
                'protocol': 'scp'
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
            protocol='scp',
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin',
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
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''',
                    f'''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  {filler}test.bin
                                1940303872 bytes total (1036210176 bytes free)
                    '''
                    ]),
                    'copy scp://127.0.0.1//path/' + filler + 'test.bin bootflash:': iter(['Copied file'])
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
                'protocol': 'scp'
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
            protocol='scp',
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/{filler}test.bin bootflash:',
                 prompt_recovery=False, timeout=300, reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_unique_file_name(self):
        filler = 'a' * 125

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:': iter([
                    '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''',
                    f'''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  {filler}test_1.bin
                                1940303872 bytes total (1036210176 bytes free)
                    '''
                    ]),
                    'copy scp://127.0.0.1//path/' + filler + 'test.bin bootflash:': iter(['Copied file'])
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
                'protocol': 'scp'
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
            protocol='scp',
            unique_file_name=True,
            unique_number=1,
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/{filler}test.bin bootflash:',
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
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''',
                    '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  test.bin_0
                                1940303872 bytes total (1036210176 bytes free)
                    '''
                    ]),
                    'copy scp://127.0.0.1//my/test.bin bootflash:': iter(['']),
                    'copy scp://127.0.0.1/' + '/path/' + 'a' * 125 + 'test.bin bootflash:/test.bin_0': iter(['Copied file'])
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
                'protocol': 'scp'
            }
        })

        self.device.testbed = testbed

        file_path = '/path/' + 'a' * 125 +  'test.bin'

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(
            steps=steps, device=self.device,
            origin=dict(
                files=[file_path],
                hostname='server1'
            ),
            destination=dict(
                directory='bootflash:'
            ),
            protocol='scp',
            rename_images='test.bin'
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1/{file_path} bootflash:/test.bin_0',
                 prompt_recovery=False, timeout=300, reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])
