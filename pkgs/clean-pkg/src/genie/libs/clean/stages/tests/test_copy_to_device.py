import unittest

from unittest.mock import Mock, call, ANY, patch

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


    def test_copy_to_device_skip_deletion_true(self):
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
        with self.assertLogs(level='INFO') as log:
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
                skip_deletion=True
            )
            self.assertIn(f"INFO:pyats.aetest.steps.implementation:Skipped reason: Skip verifying free space on the device '{self.device.name}' because skip_deletion is set to True",
                          log.output)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin',
                 prompt_recovery=False, timeout=300, reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])


    def test_copy_to_device_and_with_different_size_and_overwrite_if_size_different_false(self):
        """Name exists with different size, overwrite_if_size_different=False -> skip copy and mark step as failed"""
        # prepare device API to return remote filesize, but verify_file_exists returns False (size mismatch)
        self.device.api.get_file_size_from_server = Mock(return_value=1234)
        self.device.api.verify_file_exists = Mock(return_value=False)

        # Mock execute: dir shows test.bin present
        class MockExecute:
            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:': iter([
                        '''
                            Directory of bootflash:/
                                    11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                    12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                    8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  test.bin
                                    1940303872 bytes total (1036210176 bytes free)
                        '''
                    ])
                }

            def __call__(self, cmd, *args, **kwargs):
                return next(self.data[cmd])

        self.device.execute = Mock(side_effect=MockExecute())

        steps = Steps()
        testbed = Testbed('mytb', servers={
            'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }
        })
        self.device.testbed = testbed

        with self.assertRaises(TerminateStepSignal):
            self.cls.copy_to_device(
                steps=steps, device=self.device,
                origin=dict(files=['/path/test.bin'], hostname='server1'),
                destination=dict(directory='bootflash:'),
                protocol='scp',
                overwrite=False,
                overwrite_if_size_different=False,
            )

        self.assertTrue(any(d.result == Failed for d in steps.details))

        self.device.execute.assert_has_calls([call('dir bootflash:')])
        self.assertNotIn(
            call(f'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin',
                prompt_recovery=False, timeout=300, reply=ANY, error_pattern=ANY),
            self.device.execute.mock_calls
        )

    # Mock os.stat to return a specific file size
    @patch('genie.libs.clean.stages.stages.os.stat')
    def test_copy_to_device_with_different_size_and_overwrite_if_size_different_true(
        self, mock_stat
    ):
        """Test copy_to_device with different size and overwrite_if_size_different=True"""
        # Mock local file size (correct size)
        stat_result = Mock()
        stat_result.st_size = 1234
        mock_stat.return_value = stat_result
        self.device.api.get_file_size_from_server = Mock(return_value=1234)

        # Mock verify_file_exists:
        # First call (BEFORE copy): Returns False because size mismatch (expecting 1234, found 4096)
        # Second call (AFTER copy): Returns True because size matches (1234 == 1234)
        self.device.api.verify_file_exists = Mock(side_effect=[False, True])
        self.device.api.free_up_disk_space = Mock(return_value=True)

        class MockExecute:
            def __init__(self):
                self.call_count = 0

            def __call__(self, cmd, *args, **kwargs):
                if cmd == 'dir bootflash:':
                    self.call_count += 1
                    if self.call_count == 1:
                        # First dir call (BEFORE copy): File exists with WRONG size (4096)
                        return '''
                            Directory of bootflash:/
                                    11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                    12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                    8033  -rw-            4096  Nov 25 2016 18:42:07 -07:00  test.bin
                                    1940303872 bytes total (1036210176 bytes free)
                        '''
                    else:
                        # Second dir call (AFTER copy): File has CORRECT size (1234)
                        return '''
                            Directory of bootflash:/
                                    11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                    12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                    8033  -rw-            1234  Nov 25 2016 18:42:07 -07:00  test.bin
                                    1940303872 bytes total (1036210176 bytes free)
                        '''
                return ''

        self.device.execute = Mock(side_effect=MockExecute())
        self.device.api.copy_to_device = Mock(return_value=True)
        testbed = Testbed(
            'mytb',
            servers={
                'server1': {
                    'address': '127.0.0.1',
                    'protocol': 'scp',
                }
            },
        )
        self.device.testbed = testbed
        steps = Steps()
        # Run the copy_to_device stage
        self.cls.copy_to_device(
            steps=steps,
            device=self.device,
            origin=dict(files=['/path/test.bin'], hostname='server1'),
            destination=dict(directory='bootflash:'),
            protocol='scp',
            overwrite=False,
            overwrite_if_size_different=True,  # But DO overwrite if size is different
        )

        self.assertTrue(any(s.result == Passed for s in steps.details),
                    "Stage should pass when overwrite_if_size_different=True")
        dir_calls = [c for c in self.device.execute.call_args_list if c[0][0] == 'dir bootflash:']
        self.assertEqual(len(dir_calls), 2, 
                        "dir should be called twice: before copy and after copy")
        self.device.api.copy_to_device.assert_called_once()

        # Even though user set overwrite=False, it should be True due to size_mismatch
        call_kwargs = self.device.api.copy_to_device.call_args.kwargs
        self.assertTrue(
            call_kwargs.get('overwrite', False),
            "overwrite must be True when size mismatch is detected and overwrite_if_size_different=True"
        )

        self.assertGreaterEqual(self.device.api.verify_file_exists.call_count, 2,
                            "verify_file_exists should be called at least twice: before and after copy")

        first_verify_call = self.device.api.verify_file_exists.call_args_list[0]
        self.assertEqual(first_verify_call.kwargs.get('size'), 1234,
                        "First verification should check for expected size 1234")

        last_verify_call = self.device.api.verify_file_exists.call_args_list[-1]
        self.assertEqual(last_verify_call.kwargs.get('size'), 1234,
                        "Final verification should check for expected size 1234")

        self.device.api.free_up_disk_space.assert_called_once()

        self.assertTrue(mock_stat.called, "os.stat should be called to get local file size")

    def test_copy_to_device_with_permission_denied_retry(self):
        """Test that copy retries with unique filename when permission denied error occurs"""
        
        copy_attempt = {'count': 0}
        verify_call_count = {'count': 0}
        
        class MockExecute:
            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:': iter([
                        '''
                            Directory of bootflash:/
                                    11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                    1940303872 bytes total (1036210176 bytes free)
                        ''',
                        '''
                            Directory of bootflash:/
                                    11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                    8034  drwx             4096  Nov 25 2016 18:45:10 -07:00  test_123456.bin
                                    1940303872 bytes total (1036210176 bytes free)
                        '''
                    ])
                }

            def __call__(self, cmd, *args, **kwargs):
                if 'dir' in cmd:
                    return next(self.data['dir bootflash:'])
                
                # First copy attempt raises permission denied error
                if copy_attempt['count'] == 0:
                    copy_attempt['count'] += 1
                    raise Exception('Permission denied. Cannot overwrite existing file.')
                
                # Second attempt with unique filename succeeds
                return 'Copied file successfully'

        def mock_verify_file_exists(*args, **kwargs):
            """Return False initially to trigger copy, True after retry for verification"""
            verify_call_count['count'] += 1
            # First call: return False to trigger copy
            # Second call (after retry): return True for verification
            return verify_call_count['count'] > 1

        self.device.execute = Mock(side_effect=MockExecute())
        self.device.api.modify_filename = Mock(return_value='test_123456.bin')
        self.device.api.verify_file_exists = Mock(side_effect=mock_verify_file_exists)

        steps = Steps()
        testbed = Testbed('mytb', servers={'server1': {'address': '127.0.0.1', 'protocol': 'scp'}})
        self.device.testbed = testbed

        self.cls.copy_to_device(
            steps=steps, device=self.device,
            origin=dict(files=['/path/test.bin'], hostname='server1'),
            destination=dict(directory='bootflash:'),
            protocol='scp',
        )

        # Verify successful retry
        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(copy_attempt['count'], 1)
        # Verify modify_filename was called for retry
        self.device.api.modify_filename.assert_called()

