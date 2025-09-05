import unittest

from unittest.mock import Mock, call, ANY, patch, mock_open

from genie.libs.clean.stages.iosxe.stages import CopyToDevice
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped, Passx
from pyats.aetest.signals import TerminateStepSignal, AEtestStepSkippedSignal, AEtestSkippedSignal
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
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
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
                    'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin':
                    iter(['Copied file']),
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(steps=steps,
                                device=self.device,
                                origin=dict(files=[f'/path/test.bin'],
                                            hostname='server1'),
                                destination=dict(directory='bootflash:'),
                                protocol='scp',
                                verify_running_image=False)
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin',
                 prompt_recovery=False,
                 timeout=300,
                 reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_do_not_skip_copy_to_device_for_smu(self):

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  smu.bin
                                1940303872 bytes total (1036210176 bytes free)
                    '''
                    ]),
                    'copy tftp://127.0.0.1//path/smu.bin bootflash:/smu.bin':
                    iter(['Copied file']),
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'tftp'
            }})

        self.device.testbed = testbed

        # And we want the parse method to be mocked with expected dict
        self.device.parse = Mock(return_value={'version': {'build_label': 'TEST_LATEST_IMAGE_20230606', \
         'version_short': '17.7', 'platform': 'Catalyst L3 Switch', 'version': '17.7.1', 'image_id': 'CAT9K_IOSXE',\
         'label': 'RELEASE SOFTWARE', 'os': 'IOS-XE', 'image_type': 'production image', 'copyright_years': '1986-2021'}})

        # Mock the get_running_image api to simulate the scenario
        self.device.api.get_running_image = Mock(
            return_value='cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin')

        # Mock the apis to simulate the scenario
        self.device.api.free_up_disk_space = Mock(return_value=True)
        mock_function = Mock()
        mock_function.side_effect = [False, True]
        self.device.api.verify_file_exists = Mock(side_effect=mock_function)

        self.device.api.get_file_size_from_server = Mock(return_value=True)

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(
            steps=steps,
            device=self.device,
            origin=dict(files=[
                '/path/cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin',
                '/path/smu.bin'
            ],
                        hostname='server1'),
            destination=dict(directory='bootflash:'),
            protocol='tftp',
            verify_running_image=True)

        # Check that the result is expected
        self.assertEqual("Verify the image running in the device",
                         steps.details[1].name)
        # Check if the base image copy is skipped
        self.assertEqual(Passx, steps.details[1].result)
        # check if SMU image has been copied
        self.assertEqual(
            "Copying image file /path/smu.bin to device PE1 bootflash:",
            steps.details[13].name)
        # check if image copy succeeded
        self.assertEqual(Passed, steps.details[13].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy tftp://127.0.0.1//path/smu.bin bootflash:/smu.bin',
                 prompt_recovery=False,
                 timeout=300,
                 reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_long_filename(self):
        filler = 'a' * 125

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
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
                    'copy scp://127.0.0.1//path/' + filler + 'test.bin bootflash:':
                    iter(['Copied file'])
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(steps=steps,
                                device=self.device,
                                origin=dict(files=[f'/path/{filler}test.bin'],
                                            hostname='server1'),
                                destination=dict(directory='bootflash:'),
                                protocol='scp',
                                verify_running_image=False)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/{filler}test.bin bootflash:',
                 prompt_recovery=False,
                 timeout=300,
                 reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_unique_file_name(self):
        filler = 'a' * 125

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
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
                    'copy scp://127.0.0.1//path/' + filler + 'test.bin bootflash:':
                    iter(['Copied file'])
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(steps=steps,
                                device=self.device,
                                origin=dict(files=[f'/path/{filler}test.bin'],
                                            hostname='server1'),
                                destination=dict(directory='bootflash:'),
                                protocol='scp',
                                unique_file_name=True,
                                unique_number=1,
                                verify_running_image=False)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/{filler}test.bin bootflash:',
                 prompt_recovery=False,
                 timeout=300,
                 reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_rename_images(self):

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', '''
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
                    'copy scp://127.0.0.1//my/test.bin bootflash:':
                    iter(['']),
                    'copy scp://127.0.0.1/' + '/path/' + 'a' * 125 + 'test.bin bootflash:/test.bin_0':
                    iter(['Copied file'])
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed

        file_path = '/path/' + 'a' * 125 + 'test.bin'

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(steps=steps,
                                device=self.device,
                                origin=dict(files=[file_path],
                                            hostname='server1'),
                                destination=dict(directory='bootflash:'),
                                protocol='scp',
                                rename_images='test.bin',
                                verify_running_image=False)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1/{file_path} bootflash:/test.bin_0',
                 prompt_recovery=False,
                 timeout=300,
                 reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_verify_running_image_1(self):
        """
        To test the verify_running_image args (set default to: True)
        """
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        testbed = Testbed(
            'mytb',
            servers={'tftp': {
                'address': '127.0.0.1',
                'protocol': 'tftp'
            }})
        self.device.testbed = testbed

        # And we want the parse method to be mocked with expected dict
        self.device.parse = Mock(return_value={'version': {'build_label': 'TEST_LATEST_IMAGE_20230606', \
         'version_short': '17.7', 'platform': 'Catalyst L3 Switch', 'version': '17.7.1', 'image_id': 'CAT9K_IOSXE',\
         'label': 'RELEASE SOFTWARE', 'os': 'IOS-XE', 'image_type': 'production image', 'copyright_years': '1986-2021'}})

        # Mock the get_running_image api to simulate the scenario
        self.device.api.get_running_image = Mock(
            return_value='cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin')

        # Check if the stage raises skipped signal when the provided image matches the current running image on the device
        with self.assertRaises(AEtestSkippedSignal):
            # Call the method to be tested (clean step inside class)
            self.cls.copy_to_device(
                steps=steps,
                device=self.device,
                origin=dict(files=[
                    f'/path/cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin'
                ],
                            hostname='127.0.0.1'),
                destination=dict(directory='bootflash:'),
                protocol='tftp',
                vrf='Mgmt-vrf')

        self.assertEqual(
            self.cls.history['CopyToDevice'].parameters['image_mapping'], {
                '/path/cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin':
                'bootflash:/cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin'
            })

    def test_copy_to_device_verify_running_image_2(self):
        """
        To Test if the device is in bundle mode and user passed install_image stage in clean file
        this step should be skipped.
        """

        # Make sure we have a unique Steps() object for result verification

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
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
                    'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin':
                    iter(['Copied file']),
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed

        # clean stages order
        self.device.clean.order = ['connect', 'install_image']

        # And we want the parse method to be mocked with expected dict
        self.device.parse = Mock(return_value={'version': {'xe_version': 'test.bin',\
         'version_short': '17.7'}, 'switch_num': {'1': {'ports': '120', 'sw_image': 'CAT9K_IOSXE', 'installation_mode': 'BUNDLE'}}})

        # Mock the apis to simulate the scenario
        self.device.api.free_up_disk_space = Mock(return_value=True)

        self.device.api.verify_file_exists = Mock(return_value=True)

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(
            steps=steps,
            device=self.device,
            origin=dict(files=[f'/path/test.bin'], hostname='server1'),
            destination=dict(directory='bootflash:'),
            protocol='tftp',
        )

        skipped_reason = 'The device is in bundle mode and install_image stage is passed in clean file. Skipping the verify running image check.'

        # Check that the result is expected
        self.assertEqual("Verify the image running in the device",
                         steps.details[1].name)
        self.assertEqual(Skipped, steps.details[1].result)
        self.assertEqual(skipped_reason, steps.details[1].result.reason)

    def test_copy_to_device_verify_running_image_3(self):
        """
        To Test if the device is in bundle mode and user passed install_image stage in clean file
        this step should be skipped.
        """

        # Make sure we have a unique Steps() object for result verification

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
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
                    'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin':
                    iter(['Copied file']),
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed

        # clean stages order
        self.device.clean.order = ['connect', 'install_image']

        # And we want the parse method to be mocked with expected dict
        self.device.parse = Mock(return_value={'version': {'xe_version': 'test.bin',\
         'version_short': '17.7'}, 'switch_num': {'1': {'ports': '120', 'sw_image': 'CAT9K_IOSXE', 'mode': 'BUNDLE'}}})

        # Mock the apis to simulate the scenario
        self.device.api.free_up_disk_space = Mock(return_value=True)

        self.device.api.verify_file_exists = Mock(return_value=True)

        # Call the method to be tested (clean step inside class)
        self.cls.copy_to_device(
            steps=steps,
            device=self.device,
            origin=dict(files=[f'/path/test.bin'], hostname='server1'),
            destination=dict(directory='bootflash:'),
            protocol='tftp',
        )

        skipped_reason = 'The device is in bundle mode and install_image stage is passed in clean file. Skipping the verify running image check.'

        # Check that the result is expected
        self.assertEqual("Verify the image running in the device",
                         steps.details[1].name)
        self.assertEqual(Skipped, steps.details[1].result)
        self.assertEqual(skipped_reason, steps.details[1].result.reason)

    def test_copy_to_device_skip_deletion_true(self):

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
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
                    'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin':
                    iter(['Copied file']),
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed

        # Call the method to be tested (clean step inside class)
        with self.assertLogs(level='INFO') as log:
            self.cls.copy_to_device(steps=steps,
                                    device=self.device,
                                    origin=dict(files=[f'/path/test.bin'],
                                                hostname='server1'),
                                    destination=dict(directory='bootflash:'),
                                    protocol='scp',
                                    verify_running_image=False,
                                    skip_deletion=True)
            self.assertIn(
                f"INFO:pyats.aetest.steps.implementation:Skipped reason: Skip verifying free space on the device '{self.device.name}' because skip_deletion is set to True",
                log.output)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin',
                 prompt_recovery=False,
                 timeout=300,
                 reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_verify_md5_hash_pass(self):
        """
        To test the verify_running_image args (set default to: True)
        """
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        testbed = Testbed('mytb',
                          servers={
                              'tftp': {
                                  'address': '127.0.0.1',
                                  'protocol': 'tftp'
                              },
                              'proxy': {
                                  'address': '127.0.0.1',
                                  'protocol': 'scp'
                              }
                          })

        self.device.testbed = testbed

        # Mock the get_running_image api to simulate the scenario
        self.device.api.get_running_image = Mock(
            return_value='cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin')
        self.device.api.get_md5_hash_of_file = Mock(return_value='12345abcde')
        # And we want the parse method to be mocked with expected dict
        self.device.parse = Mock(return_value={'version': {'xe_version': 'test.bin',\
         'version_short': '17.7'}, 'switch_num': {'1': {'ports': '120', 'sw_image': 'CAT9K_IOSXE', 'mode': 'BUNDLE'}}})

        server = Mock()
        self.device.api.convert_server_to_linux_device = Mock(
            return_value=server)
        server.api.get_md5_hash_of_file = Mock(return_value='12345abcde')

        # Check if the stage raises skipped signal when the provided image matches the current running image on the device
        with self.assertRaises(AEtestSkippedSignal):
            # Call the method to be tested (clean step inside class)
            self.cls.copy_to_device(
                steps=steps,
                device=self.device,
                origin=dict(files=[
                    f'/path/cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin'
                ],
                            hostname='127.0.0.1'),
                destination=dict(directory='bootflash:'),
                protocol='tftp',
                vrf='Mgmt-vrf',
                verify_md5={
                    'verify_host': 'proxy',
                    'enable': True,
                })

    def test_copy_to_device_verify_md5_hash_pass_local(self):
        """
        To test the verify_running_image args (set default to: True)
        """
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        testbed = Testbed(
            'mytb',
            servers={'tftp': {
                'address': '127.0.0.1',
                'protocol': 'tftp'
            }})

        self.device.testbed = testbed
        # And we want the parse method to be mocked with expected dict
        self.device.parse = Mock(return_value={'version': {'xe_version': 'test.bin',\
         'version_short': '17.7'}, 'switch_num': {'1': {'ports': '120', 'sw_image': 'CAT9K_IOSXE', 'mode': 'BUNDLE'}}})

        # Mock the get_running_image api to simulate the scenario
        self.device.api.get_running_image = Mock(
            return_value='cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin')
        self.device.api.get_md5_hash_of_file = Mock(return_value='12345abcde')

        # Check if the stage raises skipped signal when the provided image matches the current running image on the device
        with self.assertRaises(AEtestSkippedSignal):
            # Call the method to be tested (clean step inside class)
            with patch("builtins.open", mock_open()) as mock_file:
                mock_file.read = Mock()
                with patch("hashlib.md5") as hash_:
                    hash_().hexdigest.return_value = "12345abcde"
                    self.cls.copy_to_device(
                        steps=steps,
                        device=self.device,
                        origin=dict(files=[
                            f'/path/cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin'
                        ],
                                    hostname='127.0.0.1'),
                        destination=dict(directory='bootflash:'),
                        protocol='tftp',
                        vrf='Mgmt-vrf',
                        verify_md5={'enable': True})

    def test_copy_to_device_verify_install_mode(self):
        """
        To test the verify_running_image args (set default to: True)
        """

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
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
                    'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin':
                    iter(['Copied file']),
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()
        # And we want the parse method to be mocked with expected dict
        self.device.parse = Mock(return_value={'version': {'xe_version': 'test.bin',\
         'version_short': '17.7'}, 'switch_num': {'1': {'ports': '120', 'sw_image': 'CAT9K_IOSXE', 'mode': 'INSTALL'}}})

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed
        # Mock the get_running_image api to simulate the scenario
        self.device.api.get_running_image = Mock(
            return_value='cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin')

        self.device.api.get_md5_hash_of_file = Mock(return_value='12345abcde')
        # Mock the apis to simulate the scenario
        self.device.api.free_up_disk_space = Mock(return_value=True)
        mock_function = Mock()
        mock_function.side_effect = [False, True]
        self.device.api.verify_file_exists = Mock(side_effect=mock_function)

        self.device.api.get_file_size_from_server = Mock(return_value=True)

        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.read = Mock()
            with patch("hashlib.md5") as hash_:
                hash_().hexdigest.return_value = "1234"

                self.cls.copy_to_device(
                    steps=steps,
                    device=self.device,
                    origin=dict(files=[f'/path/test.bin'], hostname='server1'),
                    destination=dict(directory='bootflash:'),
                    protocol='scp',
                    verify_running_image=False,
                    verify_md5={'enable': True})
        # Check that the result is expected
        self.assertEqual(Passx, steps.details[1].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin',
                 prompt_recovery=False,
                 timeout=300,
                 reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])

    def test_copy_to_device_verify_hash_not_match(self):
        """
        To test the verify_running_image args (set default to: True)
        """

        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'dir bootflash:':
                    iter([
                        '''
                        Directory of bootflash:/
                                11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                                12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                                104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                                80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                                64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                                48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                                1940303872 bytes total (1036210176 bytes free)
                    ''', f'''
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
                    'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin':
                    iter(['Copied file']),
                }

            def __call__(self, cmd, *args, **kwargs):
                output = next(self.data[cmd])
                return output

        mock_execute = MockExecute()
        # And we want the parse method to be mocked with expected dict
        self.device.parse = Mock(return_value={'version': {'xe_version': 'test.bin',\
         'version_short': '17.7'}, 'switch_num': {'1': {'ports': '120', 'sw_image': 'CAT9K_IOSXE', 'mode': 'BUNDLE'}}})

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        testbed = Testbed(
            'mytb',
            servers={'server1': {
                'address': '127.0.0.1',
                'protocol': 'scp'
            }})

        self.device.testbed = testbed
        # Mock the get_running_image api to simulate the scenario
        self.device.api.get_running_image = Mock(
            return_value='cat9k_iosxe.TEST_LATEST_IMAGE_20230606.SSA.bin')

        self.device.api.get_md5_hash_of_file = Mock(return_value='12345abcde')
        # Mock the apis to simulate the scenario
        self.device.api.free_up_disk_space = Mock(return_value=True)
        mock_function = Mock()
        mock_function.side_effect = [False, True]
        self.device.api.verify_file_exists = Mock(side_effect=mock_function)

        self.device.api.get_file_size_from_server = Mock(return_value=True)

        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.read = Mock()
            with patch("hashlib.md5") as hash_:
                hash_().hexdigest.return_value = "1234"

                self.cls.copy_to_device(
                    steps=steps,
                    device=self.device,
                    origin=dict(files=[f'/path/test.bin'], hostname='server1'),
                    destination=dict(directory='bootflash:'),
                    protocol='scp',
                    verify_running_image=False,
                    verify_md5={'enable': True})
        # Check that the result is expected
        self.assertEqual(Passx, steps.details[1].result)
        self.device.execute.assert_has_calls([
            call('dir bootflash:'),
            call(f'copy scp://127.0.0.1//path/test.bin bootflash:/test.bin',
                 prompt_recovery=False,
                 timeout=300,
                 reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])
