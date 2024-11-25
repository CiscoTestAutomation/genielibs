import unittest

from unittest.mock import Mock, call, ANY

from genie.libs.clean.stages.apic.stages import CopyToDevice
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
        self.device = create_test_device('PE1', os='apic', via='cli')

        # And we want the connect method to be mocked.
        # This simulates the pass case.
        self.device.connect = Mock()


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
                    'scp None@127.0.0.1:/path/test.bin bootflash:/test.bin': iter(['Copied file']),
                    'show version': iter([
                    '''
                        Role        Pod         Node        Name                      Version              
                        ----------  ----------  ----------  ------------------------  -------------------- 
                        controller  1           1           msl-ifav205-ifc1          5.1(2e)              
                        leaf        1           101         msl-ifav205-leaf1         n9000-15.1(2e)       
                        spine       1           201         msl-ifav205-spine1        n9000-15.1(2e)       
                        spine       1           202         msl-ifav205-spine2        n9000-14.2(2e)   
                    '''
                    ]),
                    'ls -l bootflash:': iter([
                    '''
                        total 6894908
                        lrwxrwxrwx 1 root  root          12 Mar 23 23:36 aci -> /.aci/viewfs
                        -rw-r--r-- 1 admin admin 7060381696 Apr  7 01:41 aci-apic-dk9.5.1.2e.iso
                        lrwxrwxrwx 1 root  root          13 Mar 23 23:36 debug -> /.aci/debugfs
                        lrwxrwxrwx 1 root  root          11 Mar 23 23:36 mit -> /.aci/mitfs
                        lrwxrwxrwx 1 root  root          11 Mar 23  2009 nonaci
                    '''
                    ])
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
                verify_running_image=False,
                skip_deletion=True
            )
            self.assertIn(f"INFO:pyats.aetest.steps.implementation:Skipped reason: Skip verifying free space on the device '{self.device.name}' because skip_deletion is set to True",
                          log.output)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('show version'),
            call('ls -l bootflash:'),
            call(f'scp None@127.0.0.1:/path/test.bin bootflash:/test.bin',
                 prompt_recovery=True, timeout=300, reply=ANY,
                 error_pattern=ANY),
            call('dir bootflash:')
        ])
