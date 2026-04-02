import re
import unittest

from unittest import mock
from unittest.mock import Mock, MagicMock, ANY, patch

from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure
from pyats.topology.credentials import Credentials

from pyats.results import Passed, Failed, Skipped
from pyats.aetest.steps import Steps
from pyats.aetest.signals import TerminateStepSignal, AEtestSkippedSignal

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.clean.stages.iosxe.stages import RommonBoot
from genie.libs.clean.stages.iosxe.cat9k.stages import UnconfigureStackwiseVirtual
from genie.metaparser.util.exceptions import SchemaEmptyParserError


RESULT_METHODS = ['passed', 'failed', 'skipped', 'passx', 'blocked', 'errored', 'aborted']


class TestRommonBoot(unittest.TestCase):

    def setUp(self):
        self.cls = RommonBoot()
        self.device = create_test_device(
            name='aDevice', os='iosxe', platform='cat9k')

    def test_delete_boot_variables_pass(self):
        steps = mock.MagicMock()
        self.device.configure = mock.Mock()

        self.cls.delete_boot_variables(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Delete configured boot variables")

        # Verify the config command was ran
        self.device.configure.assert_called_with("no boot system")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    def test_delete_boot_variables_fail(self):
        steps = mock.MagicMock()
        config_exception = Exception()

        self.device.configure = mock.Mock(side_effect=config_exception)

        self.cls.delete_boot_variables(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Delete configured boot variables")

        # Verify the config command was ran
        self.device.configure.assert_called_with("no boot system")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            'Failed to delete configured boot variables',
            from_exception=config_exception)

    def test_write_memory_pass(self):
        steps = mock.MagicMock()
        self.device.api.execute_write_memory = mock.Mock()
        self.device.execute = mock.Mock()

        self.cls.write_memory(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Write memory")

        # Verify the api was called
        self.device.api.execute_write_memory.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    def test_write_memory_fail(self):
        steps = mock.MagicMock()
        api_exception = Exception()
        self.device.api.execute_write_memory = mock.Mock(side_effect=api_exception)
        self.device.execute = mock.Mock()

        self.cls.write_memory(
            steps=steps, device=self.device)

        # Verify step name hasn't changed
        steps.start.assert_called_with("Write memory")

        # Verify the api was called
        self.device.api.execute_write_memory.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            "Failed to write memory",
            from_exception=api_exception)

    def test_go_to_rommon_pass(self):
        """Test that go_to_rommon correctly calls the device rommon method"""
        steps = mock.MagicMock()
        self.device.rommon = mock.Mock()
        self.device.is_ha = False

        self.cls.go_to_rommon(steps=steps, device=self.device)

        steps.start.assert_called_with("Bring device down to rommon mode")


        self.device.rommon.assert_called_once()

        step_context = steps.start.return_value.__enter__.return_value
        for result in RESULT_METHODS:
            if result != 'passed':
                getattr(step_context, result).assert_not_called()

    def test_rommon_boot_pass(self):
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.api.device_rommon_boot = mock.Mock()
        self.device.is_ha = False

        self.cls.rommon_boot(
            steps=steps, device=self.device, image=['bootflash:/test.bin'])

        steps.start.assert_called_with("Boot device from rommon")
        self.device.api.device_rommon_boot.assert_called_once()

    def test_rommon_boot_fail_abstraction_lookup(self):
        """Test that the stage correctly handles a failure from the boot API"""
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False

        api_exception = Exception("Boot API Failed")
        self.device.api.device_rommon_boot = mock.Mock(side_effect=api_exception)

        self.cls.rommon_boot(
            steps=steps,
            device=self.device,
            image=['bootflash:/test.bin']
        )

        self.device.api.device_rommon_boot.assert_called_once()

        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            "Failed to boot the device from rommon",
            from_exception=api_exception
        )


    def test_rommon_boot_fail_recovery_worker(self):
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False

        api_exception = Exception("Boot failed")
        self.device.api.device_rommon_boot = mock.Mock(side_effect=api_exception)

        self.cls.rommon_boot(
            steps=steps, device=self.device, image=['bootflash:/test.bin'])

        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with(
            "Failed to boot the device from rommon",
            from_exception=api_exception)

    @mock.patch('genie.libs.clean.stages.iosxe.stages._disconnect_reconnect')
    def test_reconnect_pass(self, _disconnect_reconnect):
        steps = mock.MagicMock()
        _disconnect_reconnect.return_value = True

        self.cls.reconnect(steps=steps, device=self.device)

        steps.start.assert_called_with("Reconnect to device")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    @mock.patch('genie.libs.clean.stages.iosxe.stages._disconnect_reconnect')
    def test_reconnect_fail(self, _disconnect_reconnect):
        steps = mock.MagicMock()
        _disconnect_reconnect.return_value = False

        self.cls.reconnect(steps=steps, device=self.device)

        steps.start.assert_called_with("Reconnect to device")

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value
        step_context.failed.assert_called_with("Failed to reconnect")

    def test_rommon_boot_tftp_with_retry_params(self):
        """Test that TFTP boot retry parameters are passed to the API"""
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.api.device_rommon_boot = mock.Mock()
        self.device.is_ha = False
        self.device.clean = {}

        mock_testbed = mock.MagicMock()
        mock_testbed.credentials = Credentials()
        self.device.testbed = mock_testbed

        self.device.management = {
            'address': {
                'ipv4': mock.MagicMock(ip='10.1.1.1', netmask='255.255.255.0')
            },
            'gateway': {'ipv4': '10.1.1.254'}
        }

        self.device.testbed.servers = {'tftp': {'address': '10.1.1.100'}}

        tftp_config = {'image': ['test.bin']}

        self.cls.rommon_boot(
            steps=steps,
            device=self.device,
            tftp=tftp_config,
            tftp_boot_max_attempts=5,
            tftp_boot_sleep_interval=45
        )

        # Verify that device_rommon_boot was called with the expected parameters
        self.device.api.device_rommon_boot.assert_called_once()
        call_kwargs = self.device.api.device_rommon_boot.call_args.kwargs

        # Check that key parameters are present
        self.assertIn('tftp_boot', call_kwargs)
        self.assertEqual(call_kwargs['golden_image'], None)
        self.assertIn('grub_activity_pattern', call_kwargs)
        self.assertIn('timeout', call_kwargs)
        
        passed_tftp = call_kwargs['tftp_boot']
        self.assertEqual(passed_tftp['image'], ['test.bin'])


class UnconfigureStackwiseVirtualC9500Test(unittest.TestCase):

    def setUp(self):
        self.cls = UnconfigureStackwiseVirtual()
        self.device = create_test_device(
            'PE1',
            os='iosxe',
            platform='cat9k',
            model='c9500',
        )

    # ---------------------------------------------------------
    # check_stackwise_virtual_config
    # ---------------------------------------------------------

    def test_check_stackwise_virtual_config_exists(self):
        steps = Steps()

        subconn1 = Mock()
        subconn2 = Mock()

        subconn1.execute.return_value = "svl output"
        subconn2.execute.return_value = "svl output"

        self.device.subconnections = [subconn1, subconn2]
        self.device.parse = Mock(return_value={
            'switch': {
                1: {
                    'svl': {
                        1: {
                            'ports': {
                                'TenGigabitEthernet1/0/1': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                                'TenGigabitEthernet1/0/2': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                            }
                        }
                    }
                },
                2: {
                    'svl': {
                        1: {
                            'ports': {
                                'TenGigabitEthernet2/0/1': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                                'TenGigabitEthernet2/0/2': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                            }
                        }
                    }
                },
            }
        })

        self.cls.check_stackwise_virtual_config(
            steps=steps,
            device=self.device
        )

        self.assertEqual(Passed, steps.details[0].result)


    def test_check_stackwise_virtual_config_not_exists(self):
        steps = Steps()

        subconn1 = Mock()
        subconn2 = Mock()

        subconn1.execute.return_value = "no svl"
        subconn2.execute.return_value = "no svl"

        def parse_side_effect(*args, **kwargs):
            raise SchemaEmptyParserError(
                data={}, command="show stackwise-virtual link"
            )

        self.device.subconnections = [subconn1, subconn2]
        self.device.parse = Mock(side_effect=parse_side_effect)

        # Since NO member has SVL, stage must SKIP
        with self.assertRaises(AEtestSkippedSignal):
            self.cls.check_stackwise_virtual_config(
                steps=steps,
                device=self.device
            )


    # ---------------------------------------------------------
    # unconfigure_stackwise_virtual
    # ---------------------------------------------------------

    def test_unconfigure_stackwise_virtual_with_interfaces(self):
        """Test unconfigure when parse shows SVL config with interfaces
        on multiple members."""
        steps = Steps()

        subconn1 = Mock()
        subconn2 = Mock()
        subconn1.alias = 'a'
        subconn2.alias = 'b'

        subconn1.configure = Mock(return_value=None)
        subconn2.configure = Mock(return_value=None)
        subconn1.execute = Mock(return_value="svl output")
        subconn2.execute = Mock(return_value="svl output")

        # active/standby used as ordered_connections
        self.device.active = subconn1
        self.device.standby = subconn2
        self.device.subconnections = [subconn1, subconn2]

        self.device.parse = Mock(return_value={
            'switch': {
                1: {
                    'svl': {
                        1: {
                            'ports': {
                                'TenGigabitEthernet1/0/1': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                                'TenGigabitEthernet1/0/2': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                            }
                        }
                    }
                },
                2: {
                    'svl': {
                        1: {
                            'ports': {
                                'TenGigabitEthernet2/0/1': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                                'TenGigabitEthernet2/0/2': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                            }
                        }
                    }
                },
            }
        })

        self.cls.unconfigure_stackwise_virtual(
            steps=steps,
            device=self.device
        )

        # Per interface unconfigure calls on active (subconn1)
        subconn1.configure.assert_any_call([
            'interface TenGigabitEthernet1/0/1',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn1.configure.assert_any_call([
            'interface TenGigabitEthernet1/0/2',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn1.configure.assert_any_call([
            'interface TenGigabitEthernet2/0/1',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn1.configure.assert_any_call([
            'interface TenGigabitEthernet2/0/2',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)

        # Per interface unconfigure calls on standby (subconn2)
        subconn2.configure.assert_any_call([
            'interface TenGigabitEthernet1/0/1',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn2.configure.assert_any_call([
            'interface TenGigabitEthernet1/0/2',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn2.configure.assert_any_call([
            'interface TenGigabitEthernet2/0/1',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn2.configure.assert_any_call([
            'interface TenGigabitEthernet2/0/2',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)

        # Global SVL removal on both connections
        subconn1.configure.assert_any_call(
            "no stackwise-virtual", timeout=120, reply=ANY)
        subconn2.configure.assert_any_call(
            "no stackwise-virtual", timeout=120, reply=ANY)

        # Copy running-config startup-config on both
        subconn1.execute.assert_any_call(
            "copy running-config startup-config", reply=ANY)
        subconn2.execute.assert_any_call(
            "copy running-config startup-config", reply=ANY)

        self.assertEqual(Passed, steps.details[0].result)


    # ---------------------------------------------------------
    # reload_device
    # ---------------------------------------------------------


    @patch('genie.libs.clean.stages.iosxe.cat9k.stages._disconnect_reconnect',
           return_value=True)
    @patch('genie.libs.clean.stages.iosxe.cat9k.stages.time')
    def test_reload_device_with_recovery_power_cycle_success(self, mock_time, mock_reconnect):
        """When device_recovery info exists and power cycle succeeds,
        device_recovery_boot is called followed by reconnect."""
        steps = Steps()

        subconn1 = MagicMock()
        subconn1.alias = 'a'
        subconn1.context = {}
        subconn1.spawn = MagicMock()
        self.device.subconnections = [subconn1]

        self.device.clean = MagicMock()
        self.device.clean.get = Mock(return_value={'golden_image': 'bootflash:packages.conf'})
        self.device.api.execute_power_cycle_device = Mock(return_value=None)
        self.device.api.device_recovery_boot = Mock(return_value=None)

        self.cls.reload_device(
            steps=steps,
            device=self.device,
            wait_time=1,
            reload_time=1
        )

        self.device.api.execute_power_cycle_device.assert_called_once()
        self.device.api.device_recovery_boot.assert_called_once()
        mock_reconnect.assert_called_once_with(self.device)
        self.assertEqual(Passed, steps.details[0].result)

    @patch('genie.libs.clean.stages.iosxe.cat9k.stages._disconnect_reconnect',
           return_value=True)
    @patch('genie.libs.clean.stages.iosxe.cat9k.stages.time')
    def test_reload_device_with_recovery_power_cycle_fail_reload_fallback(self, mock_time, mock_reconnect):
        """When power cycle fails, device connects and falls back to reload."""
        steps = Steps()

        subconn1 = MagicMock()
        subconn1.alias = 'a'
        subconn1.context = {}
        subconn1.spawn = MagicMock()
        self.device.subconnections = [subconn1]

        self.device.clean = MagicMock()
        self.device.clean.get = Mock(return_value={'golden_image': 'bootflash:packages.conf'})
        self.device.api.execute_power_cycle_device = Mock(
            side_effect=Exception("Power cycle failed"))
        self.device.connect = Mock(return_value=None)

        self.cls.reload_device(
            steps=steps,
            device=self.device,
            wait_time=1,
            reload_time=1
        )

        self.device.api.execute_power_cycle_device.assert_called_once()
        self.device.connect.assert_called_once()
        subconn1.sendline.assert_called_once_with('reload')
        mock_reconnect.assert_called_once_with(self.device)


    @patch('genie.libs.clean.stages.iosxe.cat9k.stages._disconnect_reconnect',
           return_value=True)
    @patch('genie.libs.clean.stages.iosxe.cat9k.stages.time')
    def test_reload_device_success(self, mock_time, mock_reconnect):
        """When no device recovery info exists, reload is executed successfully."""
        steps = Steps()

        subconn1 = MagicMock()
        subconn1.alias = 'a'
        subconn1.context = {}
        subconn1.spawn = MagicMock()
        self.device.subconnections = [subconn1]

        self.device.clean = MagicMock()
        self.device.clean.get = Mock(return_value=None)

        self.cls.reload_device(
            steps=steps,
            device=self.device,
            wait_time=1,
            reload_time=1
        )

        subconn1.sendline.assert_called_once_with('reload')
        mock_reconnect.assert_called_once_with(self.device)
        self.assertEqual(Passed, steps.details[0].result)


    @patch('genie.libs.clean.stages.iosxe.cat9k.stages._disconnect_reconnect')
    @patch('genie.libs.clean.stages.iosxe.cat9k.stages.time')
    def test_reload_device_failure(self, mock_time, mock_reconnect):
        """Reload fails when _execute_reload encounters an error."""
        steps = Steps()

        self.device.subconnections = []
        self.device.clean = MagicMock()
        self.device.clean.get = Mock(return_value=None)

        with self.assertRaises(TerminateStepSignal):
            self.cls.reload_device(
                steps=steps,
                device=self.device,
                wait_time=0,
                reload_time=1
            )

        mock_reconnect.assert_not_called()
        self.assertEqual(Failed, steps.details[0].result)

    # ---------------------------------------------------------
    # verify_stackwise_virtual_unconfig
    # ---------------------------------------------------------

    def test_verify_stackwise_virtual_unconfig_success(self):
        """All subconnections report no SVL"""
        steps = Steps()

        subconn1 = Mock()
        subconn2 = Mock()
        subconn1.execute.return_value = "empty output"
        subconn2.execute.return_value = "empty output"

        self.device.subconnections = [subconn1, subconn2]
        self.device.parse = Mock(
            side_effect=SchemaEmptyParserError(
                data={}, command="show stackwise-virtual link"
            )
        )

        self.cls.verify_stackwise_virtual_unconfig(
            steps=steps,
            device=self.device
        )

        self.assertEqual(Passed, steps.details[0].result)
        # Verify execute was called on each subconnection
        subconn1.execute.assert_called_once_with("show stackwise-virtual link")
        subconn2.execute.assert_called_once_with("show stackwise-virtual link")

    def test_verify_stackwise_virtual_unconfig_failure(self):
        """SVL still exists on a subconnection"""
        steps = Steps()

        subconn1 = Mock()
        subconn1.execute.return_value = "svl output"

        self.device.subconnections = [subconn1]
        self.device.parse = Mock(return_value={
            'switch': {
                1: {
                    'svl': {
                        1: {
                            'ports': {
                                'TenGigabitEthernet1/0/1': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                                'TenGigabitEthernet1/0/2': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                            }
                        }
                    }
                },
                2: {
                    'svl': {
                        1: {
                            'ports': {
                                'TenGigabitEthernet2/0/1': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                                'TenGigabitEthernet2/0/2': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Ready'
                                },
                            }
                        }
                    }
                },
            }
        })

        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_stackwise_virtual_unconfig(
                steps=steps,
                device=self.device
            )

        self.assertEqual(Failed, steps.details[0].result)


class UnconfigureStackwiseVirtualC9500XTest(UnconfigureStackwiseVirtualC9500Test):
    """Run all UnconfigureStackwiseVirtual tests with model c9500x """

    def setUp(self):
        self.cls = UnconfigureStackwiseVirtual()
        self.device = create_test_device(
            'PE1',
            os='iosxe',
            platform='cat9k',
            model='c9500x',
        )

    def test_check_stackwise_virtual_config_exists(self):
        steps = Steps()

        subconn1 = Mock()
        subconn2 = Mock()

        subconn1.execute.return_value = "svl output"
        subconn2.execute.return_value = "svl output"

        self.device.subconnections = [subconn1, subconn2]
        self.device.parse = Mock(return_value={
            'switch': {
                1: {
                    'svl': {
                        1: {
                            'ports': {
                                'FourHundredGigE1/0/31': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                                'FourHundredGigE1/0/32': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                            }
                        }
                    }
                },
                2: {
                    'svl': {
                        1: {
                            'ports': {
                                'FourHundredGigE2/0/31': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                                'FourHundredGigE2/0/32': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                            }
                        }
                    }
                },
            }
        })

        self.cls.check_stackwise_virtual_config(
            steps=steps,
            device=self.device
        )

        self.assertEqual(Passed, steps.details[0].result)

    def test_unconfigure_stackwise_virtual_with_interfaces(self):
        """Test unconfigure when parse shows SVL config with interfaces on multiple members."""
        steps = Steps()

        subconn1 = Mock()
        subconn2 = Mock()
        subconn1.alias = 'a'
        subconn2.alias = 'b'

        subconn1.configure = Mock(return_value=None)
        subconn2.configure = Mock(return_value=None)
        subconn1.execute = Mock(return_value="svl output")
        subconn2.execute = Mock(return_value="svl output")

        self.device.active = subconn1
        self.device.standby = subconn2
        self.device.subconnections = [subconn1, subconn2]

        self.device.parse = Mock(return_value={
            'switch': {
                1: {
                    'svl': {
                        1: {
                            'ports': {
                                'FourHundredGigE1/0/31': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                                'FourHundredGigE1/0/32': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                            }
                        }
                    }
                },
                2: {
                    'svl': {
                        1: {
                            'ports': {
                                'FourHundredGigE2/0/31': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                                'FourHundredGigE2/0/32': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                            }
                        }
                    }
                },
            }
        })

        self.cls.unconfigure_stackwise_virtual(
            steps=steps,
            device=self.device
        )

        # Per interface unconfigure calls on active (subconn1)
        subconn1.configure.assert_any_call([
            'interface FourHundredGigE1/0/31',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn1.configure.assert_any_call([
            'interface FourHundredGigE1/0/32',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn1.configure.assert_any_call([
            'interface FourHundredGigE2/0/31',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn1.configure.assert_any_call([
            'interface FourHundredGigE2/0/32',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)

        # Per interface unconfigure calls on standby (subconn2)
        subconn2.configure.assert_any_call([
            'interface FourHundredGigE1/0/31',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn2.configure.assert_any_call([
            'interface FourHundredGigE1/0/32',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn2.configure.assert_any_call([
            'interface FourHundredGigE2/0/31',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)
        subconn2.configure.assert_any_call([
            'interface FourHundredGigE2/0/32',
            'no stackwise-virtual link 1',
            'shutdown', 'exit',
        ], timeout=120, reply=ANY)

        # Global SVL removal on both connections
        subconn1.configure.assert_any_call(
            "no stackwise-virtual", timeout=120, reply=ANY)
        subconn2.configure.assert_any_call(
            "no stackwise-virtual", timeout=120, reply=ANY)

        # Copy running-config startup-config on both
        subconn1.execute.assert_any_call(
            "copy running-config startup-config", reply=ANY)
        subconn2.execute.assert_any_call(
            "copy running-config startup-config", reply=ANY)

        self.assertEqual(Passed, steps.details[0].result)

    def test_verify_stackwise_virtual_unconfig_failure(self):
        """SVL still exists on a subconnection (C9500X)"""
        steps = Steps()

        subconn1 = Mock()
        subconn1.execute.return_value = "svl output"

        self.device.subconnections = [subconn1]
        self.device.parse = Mock(return_value={
            'switch': {
                1: {
                    'svl': {
                        1: {
                            'ports': {
                                'FourHundredGigE1/0/31': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                                'FourHundredGigE1/0/32': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                            }
                        }
                    }
                },
                2: {
                    'svl': {
                        1: {
                            'ports': {
                                'FourHundredGigE2/0/31': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                                'FourHundredGigE2/0/32': {
                                    'link_status': 'Up',
                                    'protocol_status': 'Bundled'
                                },
                            }
                        }
                    }
                },
            }
        })

        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_stackwise_virtual_unconfig(
                steps=steps,
                device=self.device
            )

        self.assertEqual(Failed, steps.details[0].result)