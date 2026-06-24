import os
import unittest
from unittest.mock import Mock
from pyats.topology import loader
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.running_config.configure import configure_replace



class TestConfigureReplace(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300-24UX-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300-24UX-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_replace(self) -> None:
        result = configure_replace(self.device, 'flash:', 'new_config', '', 1, 60)
        expected_output = ('This will apply all necessary additions and deletions\r\n'
                           'to replace the current running configuration with the\r\n'
                           'contents of the specified configuration file, which is\r\n'
                           'assumed to be a complete configuration, not a partial\r\n'
                           'configuration. Enter Y if you are sure you want to proceed. ? [no]:Y')
        self.assertEqual(result, expected_output)

    def test_configure_replace_exception(self) -> None:
        with self.assertRaises(SubCommandFailure) as err:
            configure_replace(self.device, 'bootflash:', 'base_conf.conf', 'force', 1, 60)
        self.assertIn('Error: Could not open file bootflash:base_conf.conf for reading', err.exception.args[0])
        self.assertEqual(self.device.learned_hostname, '9300-24UX-2')
        self.assertEqual(self.device.hostname, '9300-24UX-2')


class TestConfigureReplaceControllerMode(unittest.TestCase):
    """Test configure_replace handling for controller mode devices"""

    def test_configure_replace_controller_mode(self):
        device = Mock()
        device.name = 'c8kv-1'
        device.state_machine = Mock()
        device.default = Mock()
        device.spawn = Mock()
        device._get_learned_hostname = Mock(return_value='c8kv-1')

        device.execute.side_effect = [
            'Router operating mode: Controller-Managed',
            '6045 bytes copied in 0.025 secs (241800 bytes/sec)',
        ]
        device.configure.return_value = 'Commit complete.'

        result = configure_replace(device, 'bootflash:', 'base.cfg', 'force', 1, 60)

        self.assertIn('Commit complete', result)
        # Verify copy was called with error_pattern
        copy_call = device.execute.call_args_list[1]
        self.assertIn('error_pattern', copy_call[1])
        self.assertEqual(copy_call[1]['error_pattern'], [r".*%Error.*"])
        # Verify configure was called correctly
        device.configure.assert_called_once_with(
            'load replace base.cfg',
            reply=unittest.mock.ANY,
            timeout=60,
            append_error_pattern=['Error:'],
        )
