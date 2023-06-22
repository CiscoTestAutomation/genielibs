import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.execute import execute_change_installed_application_state


class TestExecuteChangeInstalledApplicationState(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          dut1:
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
        self.device = self.testbed.devices['dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_change_execute_cases(self):
        # test current state UNINSTALLED
        # Go from UNINSTALLED to RUNNING
        print("Case 1")
        result = execute_change_installed_application_state(self.device, '1keyes', 'RUNNING')
        self.assertEqual(result, False)

        # test current state STOPPED
        # GO FROM STOPPED to DEPLOYED
        print("\nCase 2")
        result = execute_change_installed_application_state(self.device, '1keyes', 'DEPLOYED', 4)
        self.assertEqual(result, True)

        # test traverse forward
        # Go from DEPLOYED to RUNNING
        print("\nCase 3")
        result = execute_change_installed_application_state(self.device, '1keyes', 'running')
        self.assertEqual(result, True)

        print("\nCase 4")
        # test traverse reverse
        # test target state UNINSTALLED
        # Go from RUNNING to UNINSTALLED
        result = execute_change_installed_application_state(self.device, '1keyes', 'UNINSTALLED', 5)
        self.assertEqual(result, True)
