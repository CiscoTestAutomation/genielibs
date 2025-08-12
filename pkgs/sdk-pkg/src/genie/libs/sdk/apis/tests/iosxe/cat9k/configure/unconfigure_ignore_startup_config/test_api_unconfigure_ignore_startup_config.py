import os
from pyats.topology import loader
from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from genie.libs.sdk.apis.iosxe.cat9k.configure import unconfigure_ignore_startup_config
# Unicon
from unicon.core.errors import SubCommandFailure

class TestUnconfigureIgnoreStartupConfig(TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-c9300-64:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ott-c9300-64']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ignore_startup_config(self):
        result = unconfigure_ignore_startup_config(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_ignore_startup_config_success_second_command(self):
        """
        Test that the function successfully configures the device
        when the first command fails, but the second command succeeds.
        """
        # Configure mock_device.configure to raise SubCommandFailure on the first call,
        # and then return None (success) on the second call.
        # Patch the 'configure' method of the real self.device object
        self.mock_configure = patch.object(self.device, 'configure').start()
        # Patch the 'execute' method of the real self.device object
        self.mock_execute = patch.object(self.device, 'execute').start()
        self.mock_configure.side_effect = [
            SubCommandFailure("Simulated failure for 'no system ignore startupconfig switch all'"),
            None # This will be returned on the second call to configure
        ]

        # Call the function under test
        unconfigure_ignore_startup_config(self.device)

        # Assertions:
        # 1. Verify that 'configure' was called twice.
        self.assertEqual(self.device.configure.call_count, 2)

        # 2. Verify the specific calls made to 'configure' in order.
        expected_calls = [
            call('no system ignore startupconfig switch all'),
            call('no system ignore startupconfig')
        ]
        self.device.configure.assert_has_calls(expected_calls)

        # 3. Verify that 'execute' was not called (as it's not in rommon state)
        self.device.execute.assert_not_called()
