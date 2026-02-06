import logging
import unittest
import re
from unittest.mock import Mock, MagicMock, call, ANY, patch, PropertyMock

from genie.libs.clean.stages.iosxe.cat9k.stackwise_virtual.stages import ConfigureStackwiseVirtual
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped, Passx
from pyats.aetest.signals import TerminateStepSignal, AEtestSkippedSignal, AEtestStepPassxSignal

from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog


class ConfigureStackwiseVirtualTest(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ConfigureStackwiseVirtual()
        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1',
                                         os='iosxe',
                                         platform='cat9k',
                                         chassis_type='stackwise_virtual')

        # Mock subconnections
        self.subcon1 = MagicMock()
        self.subcon1.via = 'a'
        self.subcon2 = MagicMock()
        self.subcon2.via = 'b'
        self.device.subconnections = [self.subcon1, self.subcon2]

    def test_check_stackwise_virtual_config(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        self.device.parse = Mock(
            return_value={
                'stackwise-virtual': {
                    'link': {
                        'status':
                        'up',
                        'interfaces':
                        ['TenGigabitEthernet1/0/1', 'TenGigabitEthernet1/0/2']
                    }
                }
            })
        # Call the method to be tested (clean step inside class)
        with self.assertRaises(AEtestSkippedSignal):
            self.cls.check_stackwise_virtual_config(steps=steps,
                                                    device=self.device)

        # Check that the result is expected
        self.assertEqual(Skipped, steps.details[0].result)

        self.device.parse = Mock(side_effect=SchemaEmptyParserError(
            data={}, command="show stackwise-virtual link"))
        # Call the method to be tested (clean step inside class)
        self.cls.check_stackwise_virtual_config(
            steps=steps,
            device=self.device  # second call
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[1].result)

    def test_configure_stackwise_virtual(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        self.subcon1.execute = Mock()
        self.subcon1.parse = Mock(return_value={})
        self.subcon1.configure = Mock()

        self.subcon2.execute = Mock()
        self.subcon2.parse = Mock(return_value={})
        self.subcon2.configure = Mock()

        intf1 = MagicMock()
        intf1.stackwise_virtual_link = '1'
        intf2 = MagicMock()
        intf2.stackwise_virtual_link = '1'

        self.device.interfaces = {
            'TenGigabitEthernet1/0/1': intf1,
            'TenGigabitEthernet1/0/2': intf2,
        }

        self.device.parse = Mock()
        self.device.parse.side_effect = [
            {},  # subcon1 show stackwise-virtual
            {},  # subcon2 show stackwise-virtual
            {
                'interface': {
                    'TenGigabitEthernet1/0/1': {}
                }
            },  # subcon1 show ip int brief
            {
                'interface': {
                    'TenGigabitEthernet1/0/2': {}
                }
            },  # subcon2 show ip int brief
        ]

        # Call the method to be tested
        self.cls.configure_stackwise_virtual(steps=steps, device=self.device)

        # Verify subcon1 configured domain and its interface
        self.subcon1.configure.assert_has_calls([
            call(['stackwise-virtual', 'domain 1']),
            call([
                'interface TenGigabitEthernet1/0/1', 'stackwise-virtual link 1'
            ])
        ])

        # Verify subcon2 configured domain and its interface
        self.subcon2.configure.assert_has_calls([
            call(['stackwise-virtual', 'domain 1']),
            call([
                'interface TenGigabitEthernet1/0/2', 'stackwise-virtual link 1'
            ])
        ])

        # Verify execute calls for both subconnections
        self.subcon1.execute.assert_has_calls([
            call("show stackwise-virtual"),
            call("show ip interface brief"),
            call("copy running-config startup-config", reply=ANY)
        ])

        self.subcon2.execute.assert_has_calls([
            call("show stackwise-virtual"),
            call("show ip interface brief"),
            call("copy running-config startup-config", reply=ANY)
        ])

        # Check the overall result is as expected
        self.assertEqual(Passed, steps.details[0].result)

        # self.subcon1.execute.assert_has_calls([[call(['stackwise-virtual', 'domain 1'])

    def test_configure_stackwise_virtual_wiht_provided_interfaces(self):
        # Make sure we have a unique Steps() object for result verification

        steps = Steps()
        link_interfaces = {
            '1': ['TenGigabitEthernet1/0/1', 'TenGigabitEthernet1/0/2']
        }

        self.device.parse = Mock()

        # Mock execute and parse for domain check
        self.subcon1.execute.side_effect = [
            '',  # show stackwise-virtual (will raise SchemaEmptyParserError)
            'Interface           Status\nTenGigabitEthernet1/0/1  up\nTenGigabitEthernet1/0/2  up',  # show ip interface brief
            ''  # write memory
        ]
        self.subcon2.execute.side_effect = [
            '',  # show stackwise-virtual
            'Interface           Status\nTenGigabitEthernet1/0/1  up\nTenGigabitEthernet1/0/2  up',  # show ip interface brief
            ''  # write memory
        ]

        self.device.parse.side_effect = [
            SchemaEmptyParserError(
                'No SVL config'),  # subcon1 show stackwise-virtual
            SchemaEmptyParserError(
                'No SVL config'),  # subcon2 show stackwise-virtual
            {
                'interface': {
                    'TenGigabitEthernet1/0/1': {},
                    'TenGigabitEthernet1/0/2': {}
                }
            },  # subcon1 show ip int brief
            {
                'interface': {
                    'TenGigabitEthernet1/0/1': {},
                    'TenGigabitEthernet1/0/2': {}
                }
            },  # subcon2 show ip int brief
        ]

        # Call the method to be tested
        self.cls.configure_stackwise_virtual(steps=steps, device=self.device)

        # Verify domain configuration was called
        self.subcon1.configure.assert_any_call(
            ['stackwise-virtual', 'domain 1'])
        self.subcon2.configure.assert_any_call(
            ['stackwise-virtual', 'domain 1'])

        # Verify link configuration was called
        self.subcon1.configure.assert_any_call(
            ['interface TenGigabitEthernet1/0/1', 'stackwise-virtual link 1'])
        self.subcon1.configure.assert_any_call(
            ['interface TenGigabitEthernet1/0/2', 'stackwise-virtual link 1'])

    def test_boot_recovery(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        self.device.api.execute_power_cycle_device = Mock()
        self.device.api.device_recovery_boot = Mock()

        # Mock is_active_standby_ready utility
        with patch('unicon.plugins.iosxe.stack.utils.StackUtils.is_active_standby_ready', return_value=True) as mock_is_ready:
            # We expect this step to fail so make sure it raises the signal
            self.cls.boot_stack(steps=steps, device=self.device, wait_time=1)

            # Check the overall result is as expected
            self.assertEqual(Passed, steps.details[0].result)

            self.device.api.device_recovery_boot.assert_called_once()
            self.device.api.execute_power_cycle_device.assert_called_once()
            mock_is_ready.assert_called_once()

    def test_boot_recovery_with_reload(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        self.device.api.execute_power_cycle_device = Mock(
            side_effect=Exception("Power cycle failed"))
        self.device.api.device_recovery_boot = Mock()
        self.device.reload = Mock()
        self.device.connect = Mock()

        # Mock is_active_standby_ready utility
        with patch('unicon.plugins.iosxe.stack.utils.StackUtils.is_active_standby_ready', return_value=True) as mock_is_ready:
            # We expect this step to fail so make sure it raises the signal
            self.cls.boot_stack(steps=steps, device=self.device, wait_time=1)

            # Check the overall result is as expected
            self.assertEqual(Passed, steps.details[0].result)

            self.subcon1.sendline.assert_called_once()
            self.subcon2.sendline.assert_called_once()

            self.device.api.execute_power_cycle_device.assert_called_once()
            mock_is_ready.assert_called_once()
            # Check the overall result is as expected
            self.assertEqual(Passed, steps.details[0].result)

    def test_check_stackwise_virtual_config_with_switch_output(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # Test with switch-based output format
        self.device.parse = Mock(
            return_value={
                'switch': {
                    1: {
                        'svl': {
                            1: {
                                'ports': {
                                    'TenGigabitEthernet1/0/1': {
                                        'link_status': 'U',
                                        'protocol_status': 'R'
                                    }
                                }
                            }
                        }
                    },
                    2: {
                        'svl': {
                            1: {
                                'ports': {
                                    'TenGigabitEthernet2/0/1': {
                                        'link_status': 'U',
                                        'protocol_status': 'R'
                                    }
                                }
                            }
                        }
                    }
                }
            })
        
        # Call the method to be tested (clean step inside class)
        self.cls.verify_stack_wise_virtual_config(steps=steps,
                                                device=self.device)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        
    def test_check_stackwise_virtual_config_with_switch_output_failed(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # Test with switch-based output format
        self.device.parse = Mock(
            return_value={
                'switch': {
                    1: {
                        'svl': {
                            1: {
                                'ports': {
                                    'TenGigabitEthernet1/0/1': {
                                        'link_status': 'U',
                                        'protocol_status': 'D'
                                    }
                                }
                            }
                        }
                    },
                    2: {
                        'svl': {
                            1: {
                                'ports': {
                                    'TenGigabitEthernet2/0/1': {
                                        'link_status': 'U',
                                        'protocol_status': 'R'
                                    }
                                }
                            }
                        }
                    }
                }
            })
        
        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_stack_wise_virtual_config(steps=steps,
                                                    device=self.device)

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)